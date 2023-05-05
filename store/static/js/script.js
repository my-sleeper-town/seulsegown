/**
 * 사용자의 위치와 가까운 점포 정보를 받아 페이지를 그립니다.
 * @param {Array} jumpos - {jumpo_name: string, distance: number, position: [lat, lng], brand: string}
 * @param {string} address - 사용자의 주소
 * @param {Array} position - 사용자의 위치 [lat, lng]
 * @param {number} score - 슬세권 점수 (0~10)
 * @returns {undefined}
 */
function renderPage({ jumpos: jumpos, address: address, position: position, score: score }) {
    // 필터링을 위한 거리 값 (예시)
    const distances = [200, 300, 500];

    // 필터링 함수
    function filterJumposByDistance(jumpos, distance) {
        return jumpos.filter(jumpo => jumpo.distance <= distance);
    }

    // 필터링 결과를 저장할 객체
    const filteredJumpos = {};

    // 거리 별 필터링 결과 저장
    distances.forEach(distance => {
        filteredJumpos[distance] = filterJumposByDistance(jumpos, distance);
    });

    // html에 동적으로 결과 표시
    document.getElementById('score_result').innerHTML = `${score}점!`;
    document.getElementById('nearest-jumpo').innerHTML = `가장 가까운 편의점은 ${jumpos[0].brand}입니다`;
    document.getElementById('200m-jumpo').innerHTML = `집 근처 200미터에 ${filteredJumpos[200].length}개의 편의점이 있습니다`;
    document.getElementById('300m-jumpo').innerHTML = `집 근처 300미터에 ${filteredJumpos[300].length}개의 편의점이 있습니다`;
    document.getElementById('500m-jumpo').innerHTML = `집 근처 500미터에 ${filteredJumpos[500].length}개의 편의점이 있습니다`;
}

/**
 * 현재 위치와 점포 목록을 받아 지도를 렌더링합니다.
 * @param {Array} position - [lat, lng]
 * @param {Array} jumpos - {jumpo_name: string, distance: number, position: [lat, lng], brand: string}
 * @returns {undefined}
 */
function setMap(position, jumpos) {
    // 지도를 보여줄 div
    const mapContainer = document.getElementById('map');

    // 지도 위치 및 설정
    const map = new kakao.maps.Map(mapContainer, {
        center: new kakao.maps.LatLng(position[0], position[1]),
        level: 3,
    });

    const brandIcon = {
        cu: "/static/images/cu.png",
        emart24: "/static/images/emart24.png",
        gs25: "/static/images/gs25.png",
        ministop: "/static/images/ministop.png",
        seveneleven: "/static/images/seveneleven.png",
        default: "/static/images/markerStar.png",
    }
    const markerImage = {
        default: new kakao.maps.MarkerImage(brandIcon.default, new kakao.maps.Size(24, 35)),
        cu: new kakao.maps.MarkerImage(brandIcon.cu, new kakao.maps.Size(24, 35)),
        gs25: new kakao.maps.MarkerImage(brandIcon.gs25, new kakao.maps.Size(24, 35)),
        emart24: new kakao.maps.MarkerImage(brandIcon.emart24, new kakao.maps.Size(24, 35)),
        ministop: new kakao.maps.MarkerImage(brandIcon.ministop, new kakao.maps.Size(36, 30)),
        seveneleven: new kakao.maps.MarkerImage(brandIcon.seveneleven, new kakao.maps.Size(24, 35)),
    }

    // 유저 위치 마커 찍기
    new kakao.maps.Marker({
        map: map,
        position: new kakao.maps.LatLng(position[0], position[1]),
        image: markerImage.default
    });

    // 각 점포 별 마커 그리기
    jumpos.forEach(({ position, brand }) => {
        let image = markerImage.ministop
        switch (brand) {
            case 'CU': image = markerImage.cu; break;
            case '이마트24': image = markerImage.emart24; break;
            case '미니스톱': image = markerImage.ministop; break;
            case '세븐일레븐': image = markerImage.seveneleven; break;
            case 'GS25': image = markerImage.gs25; break;
            default: image = markerImage.default
        }
        
        new kakao.maps.Marker({
            map: map,
            position: new kakao.maps.LatLng(position[0], position[1]),
            title: brand,
            image,
        });
    })
}
