#include "Input.h"

#include "Common.h"

#include <functional>
#include <utility>

std::set<int> Input::s_keyMap;
std::set<int> Input::s_keyPressedMap;
glm::vec2 Input::s_mousePos;

GLFWwindow* Input::s_window;

void Input::handleKeyEvent(int key, int scancode, int action, int mods)
{
	if (action == GLFW_PRESS)
	{
		s_keyMap.insert(key);
		s_keyPressedMap.insert(key);
	}
	else if (action == GLFW_RELEASE)
	{
		s_keyMap.erase(key);
	}
}

glm::vec2 Input::getWindowSize()
{
	int width = 0;
	int height = 0;
	glfwGetWindowSize(s_window, &width, &height);

	return glm::vec2(width, height);
}

void Input::handleMousePosEvent(double x, double y)
{
	s_mousePos = { (float)x, (float)y };
}

void Input::setMouseVisible(bool visible)
{
	glfwSetInputMode(s_window, GLFW_CURSOR, visible ? GLFW_CURSOR_NORMAL : GLFW_CURSOR_HIDDEN);
}

void Input::setMousePos(const glm::vec2& pos)
{
	glfwSetCursorPos(s_window, pos.x, pos.y);
	s_mousePos = pos;
}

void Input::update()
{
	s_keyPressedMap.clear();
}