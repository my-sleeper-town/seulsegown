// jumpos 정보
const jumpos = [];
  
// 현재 주소와 위치 정보 (예시)
const address = '서울시 강북구 삼양로 139가길 17';
const position = [37.6500916835229, 127.012462471132];
  
// 점수 (예시)
const score = 10;
  
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