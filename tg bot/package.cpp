#include<windows.h>
#include<stdio.h>
#pragma comment( linker, "/subsystem:windows /entry:mainCRTStartup" )  

int main()
{
	system("pyinstaller -F test.py");
    return 0;
}

