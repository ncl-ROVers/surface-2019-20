#pragma once

#include "Common.h"

#include <set>

class Input
{
private:
	static std::set<int> s_keyMap;
	static std::set<int> s_keyPressedMap;
	static glm::vec2 s_mousePos;

	static GLFWwindow* s_window;
public:
	inline static bool isKeyPressed(int key) { return s_keyPressedMap.find(key) != s_keyPressedMap.end(); }
	inline static bool isKeyDown(int key) { return s_keyMap.find(key) != s_keyMap.end(); }

	static void setMouseVisible(bool visible);

	static void setMousePos(const glm::vec2& pos);
	inline static glm::vec2 getMousePos() { return s_mousePos; }

	static glm::vec2 getWindowSize();

	static void handleKeyEvent(int key, int scancode, int action, int mods);
	static void handleMousePosEvent(double x, double y);
	inline static void setWindow(GLFWwindow* window) { s_window = window; }

	static void update();
};