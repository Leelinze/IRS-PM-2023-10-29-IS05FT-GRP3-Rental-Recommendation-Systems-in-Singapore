from flask import render_template, request, redirect, url_for, current_app,jsonify
import flask_wtf as wtf
from flask_login import current_user,login_required
from app.home.models import Rating
from app.home.forms import SurveyForm,CommentForm
from app.services.DataManger import FormData
from app.home import blueprint
# from app.home.utils import *
from app.services.DataProcessing import *
from app.extension import db

@blueprint.route('/userin', methods=['GET', 'POST'])
@login_required
def userin():
    form = SurveyForm()
    return render_template('userin.html', form=form)

@blueprint.route('/get_data', methods=['GET'])
@login_required
def get_data():
    lists=current_app.recommender.get_result()
    recomm_list=current_app.data_manager.get_recommends(lists,"HouseID")
    data = recomm_list.apply(df_to_amenities, axis=1).tolist()

    return jsonify(data=data)



@blueprint.route('/recomm')
@login_required
def recomm():
    user_id = current_user.get_id()
    current_app.recommender.currUID=user_id
    checker=Rating.query.filter_by(userID=user_id).first()
    if checker:
        print("rating exists")
        current_app.recommender.mode="hybrid"
        ratingInfo=get_ratings()
        current_app.recommender.rating=ratingInfo
    else:
        print("rating not exists")
        current_app.recommender.mode="content_based"
    current_app.recommender.recommend()
    lists=current_app.recommender.get_result()
    recomm_list=current_app.data_manager.get_recommends(lists,"HouseID")
    rents=[]
    form = CommentForm()
    for row_num, row in enumerate(recomm_list.itertuples(index=False), start=1):
        dic=df_to_display(row_num, row)
        form = CommentForm()  
        dic['form'] = form  
        dic['recomm_idx'] = row_num  
        rents.append(dic)
    
    return render_template('recomm.html', rents=rents,form=form)

@blueprint.route('/submit_data', methods=['POST',"GET"])
@login_required
def submit_data():
    form = SurveyForm()
    if form.validate_on_submit():
        day_difference = int(request.form.get("dayDifference", 0)) // 30
        form_data = FormData.from_form(form, day_difference)
        current_app.map_drawer.draw_target(form_data.location[0],form_data.location[1],2,form.location.data)
        weight_vector,user_vector_w,data_vector=form_to_vecs(form_data)
        current_app.recommender.set_param(weight_vector,user_vector_w,data_vector)
        return redirect(url_for('home_blueprint.recomm')) 
       
    else:
        current_app.logger.error("验证失败：%s", form.errors)
        return redirect(url_for('home_blueprint.userin'))

@blueprint.route('/map/<int:recomm_idx>', methods=['GET'])
@login_required
def draw_map(recomm_idx):
    
    lists=current_app.recommender.get_result()
    recommendations=current_app.data_manager.get_recommends(lists,"HouseID")
    if recomm_idx < 1 or recomm_idx > len(recommendations):
        return "Place not found", 404
    place = recommendations.iloc[recomm_idx - 1]
    m=current_app.map_drawer.add_to_map(place["latitude"],place["longitude"],2,place["HouseName"],place["listing_url"],place["picture_url"])

    return m.get_root().render()

@blueprint.route('/comment/<int:recomm_idx>', methods=['GET','POST'])
@login_required
def get_comment(recomm_idx):
    lists=current_app.recommender.get_result()
    if recomm_idx < 1 or recomm_idx > len(lists):
        return "Place not found", 404
    form = CommentForm()
    if form.validate_on_submit():
        comment = form.comment.data
        rating=current_app.rating_estimator.comments_to_rating(comment)
        user_id = current_user.get_id()
        record=Rating(userID=user_id,listing_id=lists[recomm_idx - 1],rating=rating,comments=comment)
        db.session.add(record)
        db.session.commit()
        rating_df=get_ratings()
        current_app.recommender.model_update(rating_df)
        return redirect(url_for('home_blueprint.recomm')) 
    return render_template('rent_block.html', form=form,wtf=wtf,recomm_idx=recomm_idx)