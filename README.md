# SANABI Black KakaoTalk Theme — 새 버전

이번 버전은 이전 어피치 기반 결과를 버리고, **검은색 계열**을 기본으로 잡은 새 적용 패키지입니다.

## 핵심
- 가운데 큰 SANABI 도시 이미지는 `assets/main_background.jpg`를 그대로 사용
- 사용자가 제공한 캐릭터 PNG는 `assets/tab_01~05.png`, `profile_01~03.png`로 사용
- 원본/2배 업스케일 PNG 8장도 `assets/` 안에 모두 보관
- GitHub Actions가 공식 Android 샘플 프로젝트를 받아 이미지와 색상을 적용한 뒤 APK를 만듭니다.
- 임의의 화면 레이아웃을 새로 만드는 대신, 카카오톡 테마에서 실제로 교체 가능한 리소스를 교체합니다.

## 중요한 제한
카카오톡 테마 APK는 카카오톡 본체의 화면 동작을 새로 프로그래밍하는 앱이 아닙니다.
따라서 "캐릭터 버튼을 누르면 카톡 내부의 특정 큰 사진이 다른 사진으로 바뀌는" 식의 임의 동작은 테마 리소스만으로 추가할 수 없습니다.
대신 하단 탭/프로필/배경/말풍선 등의 **테마 리소스 자체를 SANABI 이미지로 교체**합니다.

## GitHub에 넣을 것
이 폴더의 내용 그대로 저장소에 올리면 됩니다.
특히 `.github/workflows/build.yml` 위치를 절대 바꾸지 마세요.

## APK
Actions → `Build SANABI Black KakaoTalk Theme` → 성공한 실행 → Artifacts → `SANABI-Black-KakaoTalk-Theme-APK`
