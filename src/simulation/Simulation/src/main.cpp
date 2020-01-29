#include <iostream>
#include <chrono>
#include <thread>

#include "Common.h"

#include "io/Input.h"
#include "Scene.h"

void APIENTRY debugOutput(GLenum source, GLenum type, GLuint id, GLenum severity, GLsizei length, const GLchar* message, const void* userParam)
{
	std::cerr << message << std::endl;
}

int main()
{
	int width = 1280;
	int height = 720;

	//Intialize GLFW and create the window
	if (!glfwInit())
	{
		std::cerr << "Failed to intialize GLFW!" << std::endl;
		exit(1);
	}

	glfwWindowHint(GLFW_VISIBLE, GLFW_TRUE);
	glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 4);
	glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
	glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);
	glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GLFW_TRUE);
	glfwWindowHint(GLFW_SAMPLES, 4);

	GLFWwindow* window = glfwCreateWindow(width, height, "ROV Simulation", nullptr, nullptr);
	if (!window)
	{
		std::cerr << "Couldn't create GLFW window!" << std::endl;
		exit(1);
	}

	glfwMakeContextCurrent(window);
	
	int status = gladLoadGLLoader((GLADloadproc)glfwGetProcAddress);
	if (!status)
	{
		std::cerr << "Faild to load GLAD!" << std::endl;
		exit(2);
	}

	glfwSwapInterval(1);

	glfwSetKeyCallback(window, [](GLFWwindow* window, int key, int scancode, int action, int mods)
	{
		Input::handleKeyEvent(key, scancode, action, mods);
	});

	glfwSetCursorPosCallback(window, [](GLFWwindow* window, double x, double y)
	{
		Input::handleMousePosEvent(x, y);
	});

	glfwSetWindowSizeCallback(window, [](GLFWwindow* window, int width, int height)
	{
		Scene::singleton()->resize(width, height);
	});

	Input::setWindow(window);

	//Initialize scene
	glEnable(GL_DEPTH_TEST);
	glEnable(GL_CULL_FACE);
	glEnable(GL_MULTISAMPLE);
	glEnable(GL_DEBUG_OUTPUT);
	glEnable(GL_DEBUG_OUTPUT_SYNCHRONOUS);

	glDebugMessageCallback(debugOutput, nullptr);

	Scene::singleton()->init(width, height);

	//Main game loop
	double frameTime = 1.0 / 60.0f;

	double lastUpdateTime = glfwGetTime();
	double lastRenderTime = glfwGetTime();

	while (!glfwWindowShouldClose(window))
	{
		glfwPollEvents();

		double elapsedTime = glfwGetTime() - lastUpdateTime;
		lastUpdateTime = glfwGetTime();

		Scene::singleton()->update(elapsedTime);

		double currentTime = glfwGetTime();
		if (currentTime - lastRenderTime >= frameTime)
		{
			lastRenderTime = currentTime;

			Scene::singleton()->render();
			glfwSwapBuffers(window);
		}
		else
		{
			using namespace std::chrono_literals;

			std::this_thread::sleep_for(1ms);
		}

		Input::update();
	}

	//Release resources
	Scene::singleton()->destroy();

	glfwDestroyWindow(window);
	glfwTerminate();
}