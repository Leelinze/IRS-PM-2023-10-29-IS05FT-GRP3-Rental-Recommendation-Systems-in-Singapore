import folium
import json

class MapDrawer:
    def __init__(self,df,mapcenter,geojson_file_path,semantic_groups,colors):
        self.map_center=mapcenter
        self.geojson_file_path=geojson_file_path
        self.data=df
        self.semantic_groups=semantic_groups
        self.color_group_mapping = dict(zip(colors, self.semantic_groups.keys()))
        self.map=None
        self.layer_list=[]
        self.__draw_poi()
        
        # self.layer=None
        # self.tar_point=None
        # self.curr_map=self.map
        # self.curr_layer=None
        pass
    def __draw_base(self):
        self.map=folium.Map(location=self.map_center, tiles="OpenStreetMap", zoom_start=14)
        with open(self.geojson_file_path, "r", encoding="utf-8") as file:
            geojson_data = json.load(file)
        folium.GeoJson(
            geojson_data,
            highlight_function=lambda feature: {
                "fillColor": "white",
                "fillOpacity": 0.2,
            },

            name="neighbourhoods",
            style_function=lambda feature: {
                "fillColor": "#8FA998",   
                "color": "#5D4E6D",
                "weight": 2,              
                "dashArray": "5, 5",
                "fillOpacity": 0.3        
            },
            zoom_on_click=True,
            tooltip=folium.GeoJsonTooltip(fields=["neighbourhood", "neighbourhood_group"], aliases=["", ""], labels=True, sticky=False), 
        ).add_to(self.map)
        pass
    def __draw_poi(self):
        self.__draw_base()
        for color, group in self.color_group_mapping.items():
            columns = self.semantic_groups[group]
            layer = folium.FeatureGroup(name=group,show=False)
            for column in columns:
                filtered_df = self.data[self.data[column] == True].dropna(subset=['lat', 'lng'])
                for _, row in filtered_df.iterrows():
                    tooltip_content = f'<b>Name:</b> {row["name"]}<br>' \
                                    f'<b>Address:</b> {row["formatted_address"]}<br>' \
                                    f'<b>Category:</b> {group}:{column}'
                    folium.Circle([row['lat'], row['lng']], 
                                        radius=2,
                                        color=color, 
                                        fill=True, 
                                        fill_color=color, 
                                        fill_opacity=0.7,
                                        tooltip=folium.Tooltip(tooltip_content)
                                ).add_to(layer) 
            self.layer_list.append(layer)
        pass
    def draw_target(self,lat, lon, radius,name):
        # self.tar_map=self.map
        kw = {"prefix": "fa", "color": "red", "icon": "arrow-down"}
        self.tar_point=folium.Marker(
            [lat, lon],
            icon=folium.Icon(**kw),
            radius=radius,
            color='#3186cc',
            fill_color='#3186cc',
            popup=name.title()
        )
        pass 
    def __get_frame(self,name, website_url, picture_url, width, height):
        max_img_height = max(60, height - 60)
        html_content = f"""
            <div style="border: 1px solid #ccc; border-radius: 8px; overflow: hidden; text-align: center; width: {width}px; height: {height}px;">
                <img src="{picture_url}" alt="Picture" style="width: 100%; height: auto; max-height: {max_img_height}px;">
                <div style="padding: 10px;">
                    <h3 style="margin: 5px 0; font-size: 16px;">{name}</h3>
                    <a href="{website_url}" target="_blank" style="display: inline-block; text-decoration: none; color: #fff; background-color: #007bff; padding: 7px 15px; border-radius: 4px; font-size: 14px;">Go to Airbnb</a>
                </div>
            </div>
        """
        iframe = folium.IFrame(html=html_content, width=width + 20, height=height + 20)  # Added some padding
        popup = folium.Popup(iframe, max_width=width + 20)
        return popup

    def add_to_map(self, lat, lon, radius,name, website_url, picture_url, width=300, height=300):
        
        
        self.__draw_base()
        map =self.map
        for layer in self.layer_list:
                layer.add_to(map)
        layer=folium.FeatureGroup(name="details")
        self.tar_point.add_to(layer)
        self.map_center=[lat, lon]
        map.location=self.map_center
        
        popup = self.__get_frame(name,website_url, picture_url, width, height)
        kw = {"prefix": "fa", "color": "green", "icon": "house"}
        
        folium.Circle(
        location=[lat, lon],
        radius=2500,
        color="black",
        weight=1,
        fill_opacity=0.1,
        opacity=1,
        fill_color="yellow",
        fill=False,  # gets overridden by fill_color
        # popup="{} meters".format(radius),
        # tooltip="I am in meters",
        ).add_to(layer)
        folium.Marker(
            [lat, lon],
            icon=folium.Icon(**kw),
            radius=radius,
            color='#3186cc',
            fill_color='#3186cc',
            popup=popup
        ).add_to(layer)
        layer.add_to(map)
        folium.LayerControl(collapsed=False).add_to(map)
        return map