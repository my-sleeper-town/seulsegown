const mapContainer = document.getElementById('map'); // 지도를 표시할 div
const mapOption = {
    center: new kakao.maps.LatLng(37.50053631299917, 127.02738767714077), // 지도 중심좌표
    level: 7, // 지도 확대 레벨
};
const map = new kakao.maps.Map(mapContainer, mapOption); // 지도 생성 및 객체 리턴

// 마커를 표시할 위치와 내용을 가지고 있는 객체 배열입니다 
const positions = [
    {
        content: '<div>gs25</div>', 
        latlng: new kakao.maps.LatLng(37.50095515358235, 127.02794480111508)
    },
    {
        content: '<div>CU</div>', 
        latlng: new kakao.maps.LatLng(37.49974300114312, 127.02918267645417)
    },
    {
        content: '<div>이마트24</div>', 
        latlng: new kakao.maps.LatLng(34.500608472331606, 127.02705973847358)
    },
    {
        content: '<div>세븐일레븐</div>', 
        latlng: new kakao.maps.LatLng(37.50086339381458, 127.02531257574705)
    },
    {
        content: '<div>gs25</div>', 
        latlng: new kakao.maps.LatLng(37.498829187856764, 127.02616004798125)
    }
];

// 마커 이미지의 이미지 주소입니다
const imageSrc = "https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/markerStar.png"; 

for (let i = 0; i < positions.length; i++) {
    // 마커 이미지의 이미지 크기 입니다
    const imageSize = new kakao.maps.Size(24, 35); 

    // 마커 이미지를 생성합니다    
    const markerImage = new kakao.maps.MarkerImage(imageSrc, imageSize); 

    // 마커를 생성합니다
    const marker = new kakao.maps.Marker({
        map: map, // 마커를 표시할 지도
        position: positions[i].latlng, // 마커를 표시할 위치
        title : positions[i].content, // 마커에 마우스를 올리면 표시할 툴팁 내용
        image : markerImage // 마커 이미지 
    });

    // 인포윈도우를 생성합니다
    const infowindow = new kakao.maps }

