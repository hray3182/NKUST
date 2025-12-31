//*** main.cpp檔案是供學生參考的範例
//*** static library使用說明 2025/11/24
// 1. 把exponentialRand.h和PKTArrivalEventGenerator.h加入專案的Header Files項目裡
// 2. 若你使用的是visual studio IDE  
//    (1)把Project_Lib.lib加入專案的Resource Files項目裡
//    (2)若要call static library裡的函數，除了一開始要include PKTArrivalEventGenerator.h，還要在function call之前加上 「#pragma comment(lib, "Project_Lib.lib")」 (參考下面範例)
// 3. 若你使用的是codeblocks
//    (1) 把libProject_Lib.a存入專案的檔案夾內
//    (2) 在 Code::Blocks 選單中，導覽至Project > Build options，然後開啟這個選項
//    (3) 在開啟的視窗中，選擇Linker Settings標籤 
//	  (4) 在"Link libraries"視窗部分，點擊Add按鈕。
//	  (5) 瀏覽到libProject_Lib.a所在的位置，然後選擇它，點擊“Open”然後"OK"。。
//    (6) 註解「#pragma comment(lib, "Project_Lib.lib")」這一行指令 (在這一行前面加上"//")