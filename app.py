from flask import Flask, render_template
import folium

app = Flask(__name__)

# ข้อมูลสถานที่ 5 จุดในจังหวัดกำแพงเพชร
LOCATIONS = [
    {
        "id": 1,
        "name": "หอประชุมทีปังกรรัศมีโชติ มหาวิทยาลัยราชภัฏกําแพงเพช",
        "category": "หอประชุม / สถานที่จัดงาน",
        "lat": 16.454657164300595,
        "lng": 99.51654562434396,
        "description": "เริ่มต้นทริปเช้าวันใหม่ที่ หอประชุมทีปังกร อาคารหอประชุมขนาดใหญ่ที่มีสถาปัตยกรรมโดดเด่น บรรยากาศเงียบสงบ เหมาะกับการแวะถ่ายรูปและเริ่มต้นการเดินทาง",
        "image": "https://atc.chula.ac.th/Main/wp-content/uploads/2022/11/kamphangphet-scaled.jpg",
        "color": "#FF6B6B",
        "icon": "building"
    },
    {
        "id": 2,
        "name": "คณะวิทยาศาสตร์และเทคโนโลยี มหาวิทยาลัยราชภัฏกำแพงเพชร",
        "category": "อาคารเรียน / การศึกษา",
        "lat": 16.455037303852983,
        "lng": 99.51027035658527,
        "description": "เดินทางต่อมายัง ตึกวิชาวิทยาศาสตร์ ศูนย์รวมความรู้เเละห้องปฏิบัติการ แวดล้อมด้วยต้นไม้ร่มรื่น สัมผัสบรรยากาศการเรียนรู้ที่ทันสมัย",
        "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTef0HalHk2KyQqTrmQSdwAOnhSsaSGuC7RpSoR1-D-8gCWiYm8Qx7guzqS&s=10",
        "color": "#4ECDC4",
        "icon": "flask"
    },
    {
        "id": 3,
        "name": "สวนสาธารณะ สิริจิตอุทยาน",
        "category": "สวนสาธารณะ / พักผ่อนหย่อนใจ",
        "lat": 16.473995917922394,
        "lng": 99.52616824685272,
        "description": "พักผ่อนช่วงบ่ายที่ สวนสาธารณะกำแพงเพชร สูดอากาศบริสุทธิ์ เดินเล่นชมวิวสระน้ำและต้นไม้ใหญ่ เหมาะสำหรับนั่งรับลมและถ่ายรูปสไตล์มินิมอล",
        "image": "https://www.educatepark.com/wp-content/uploads/2014/08/sirijit-park.jpg",
        "color": "#2ECC71",
        "icon": "tree"
    },
    {
        "id": 4,
        "name": "บิ๊กซี กำแพงเพชร",
        "category": "ศูนย์การค้า / ช้อปปิ้ง",
        "lat": 16.474797563794084,
        "lng": 99.54126470232866,
        "description": "แวะช้อปปิ้ง ทานอาหารกลางวัน หรือแวะตากแอร์เย็นๆ ที่ห้างบิ๊กซี ศูนย์รวมสินค้าและร้านอาหารหลากหลายที่สะดวกสบาย",
        "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR6jy6tT7s8ktE0R6GleRSEw-n3KYSSl4BZ8B0GyLWOczpGMMj9tooxlA4&s=10",
        "color": "#F1C40F",
        "icon": "shopping-cart"
    },
    {
        "id": 5,
        "name": "โรบินสัน กำแพงเพชร",
        "category": "ห้างสรรพสินค้า / ไลฟ์สไตล์",
        "lat": 16.475863385553588,
        "lng": 99.54942396997174,
        "description": "ปิดทริปวันสบายๆ ที่ โรบินสัน ไลฟ์สไตล์ กำแพงเพชร เดินเที่ยว ดูหนัง ช้อปปิ้งสินค้าแบรนด์เนม และทานอาหารมื้อค่ำแสนอร่อย",
        "image": "https://prod-assets.central.co.th/file-assets/assets/CMS/store/store-image/robinson-lifestyle-kamphaengphet.webp",
        "color": "#9B59B6",
        "icon": "shopping-bag"
    }
]

def create_full_gmaps_route(locations):
    """ สร้าง URL สำหรับ Google Maps Route รวมทุกสถานที่ """
    base_url = "https://www.google.com/maps/dir/"
    coords_path = "/".join([f"{loc['lat']},{loc['lng']}" for loc in locations])
    return base_url + coords_path

@app.route('/')
def index():
    # 1. พิกัดกึ่งกลางสำหรับสร้างแผนที่ Folium
    avg_lat = sum(loc['lat'] for loc in LOCATIONS) / len(LOCATIONS)
    avg_lng = sum(loc['lng'] for loc in LOCATIONS) / len(LOCATIONS)
    
    # 2. สร้างวัตถุแผนที่ Folium (ใช้ CartoDB Positron สไตล์ มินิมอล สบายตา)
    m = folium.Map(
        location=[avg_lat, avg_lng],
        zoom_start=13,
        tiles="CartoDB positron",
        control_scale=True
    )

    # 3. วาดเส้นทางการเดินทาง (Polyline)
    route_coords = [[loc['lat'], loc['lng']] for loc in LOCATIONS]
    folium.PolyLine(
        locations=route_coords,
        color="#FF7675",
        weight=4,
        opacity=0.8,
        dash_array='8, 8'
    ).add_to(m)

    # 4. ปักหมุดสถานที่ (Markers)
    for loc in LOCATIONS:
        # สร้าง HTML Popup สไตล์การ์ตูนมินิมอล
        popup_html = f"""
        <div style="font-family: 'Kanit', sans-serif; text-align: center; width: 180px; padding: 5px;">
            <b style="color: #2D3436; font-size: 14px;">จุดที่ {loc['id']}: {loc['name']}</b><br>
            <span style="color: #636E72; font-size: 11px;">{loc['category']}</span><br>
            <a href="https://www.google.com/maps/dir/?api=1&destination={loc['lat']},{loc['lng']}" 
               target="_blank" 
               style="display: inline-block; margin-top: 8px; padding: 4px 10px; background: #FF7675; color: white; text-decoration: none; border-radius: 12px; font-size: 11px; font-weight: bold;">
               🗺️ นำทาง
            </a>
        </div>
        """
        
        folium.Marker(
            location=[loc['lat'], loc['lng']],
            popup=folium.Popup(popup_html, max_width=220),
            tooltip=f"จุดที่ {loc['id']}: {loc['name']}",
            icon=folium.Icon(color="red", icon="info-sign")
        ).add_to(m)

    # แปลงแผนที่ Folium เป็น HTML String เพื่อนำไปฝังใน Jinja Template
    map_html = m._repr_html_()

    # สร้าง ลิงก์นำทาง Google Maps สำหรับรวมทุกจุด
    full_route_url = create_full_gmaps_route(LOCATIONS)

    # เพิ่ม Google Maps Link รายบุคคลเข้าไปใน Dict
    for loc in LOCATIONS:
        loc['gmaps_url'] = f"https://www.google.com/maps/dir/?api=1&destination={loc['lat']},{loc['lng']}"

    return render_template('index.html', 
                           locations=LOCATIONS, 
                           map_html=map_html, 
                           full_route_url=full_route_url)

if __name__ == '__main__':
    app.run(debug=True)