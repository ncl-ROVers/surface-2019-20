#include "Scene.h"

#include "Common.h"

#include <string>

using namespace std::string_literals;

const std::string vertexShaderCode = R"(
#version 430 core

layout(location = 0) in vec3 position;
layout(location = 1) in vec2 texCoords;

layout(location = 0) out vec2 outTexCoords;
layout(location = 1) out vec3 outWorldPos;

uniform mat4 transform;
uniform mat4 model;

void main() {
	outTexCoords = texCoords;

	outWorldPos = (model * vec4(position, 1.0)).xyz;
	gl_Position = transform * vec4(position, 1.0);
}
)";

const std::string fragmentShaderCode = R"(
#version 430 core

layout(location = 0) out vec4 outColor;

layout(location = 0) in vec2 inTexCoords;
layout(location = 1) in vec3 inWorldPos;

void main() {
	vec3 lightPos = vec3(0.0, 0.4, 0.0);
	vec3 normal = vec3(0.0, 1.0, 0.0);

	vec3 toLight = lightPos - inWorldPos;
	float lightDistance = length(toLight);
	toLight = normalize(toLight);

	float diffuse = max(dot(normal, toLight), 0) * (1.0 / (lightDistance * lightDistance));
	outColor = diffuse * vec4(1.0);
}
)";

void Scene::init(int width, int height)
{
	m_shader.init();
	m_shader.addShader(GL_VERTEX_SHADER, vertexShaderCode);
	m_shader.addShader(GL_FRAGMENT_SHADER, fragmentShaderCode);
	m_shader.compile();

	float vertices[] =
	{
		-1.0, 1.0, 0.0, 0.0, 1.0,
		-1.0, -1.0, 0.0, 0.0, 0.0,
		1.0, 1.0, 0.0, 1.0, 1.0,
		-1.0, -1.0, 0.0, 0.0, 0.0,
		1.0, -1.0, 0.0, 1.0, 0.0,
		1.0, 1.0, 0.0, 1.0, 1.0
	};

	m_vertexArray.init();
	m_vertexArray.createBuffer(GL_ARRAY_BUFFER, vertices, 6 * 5 * 4);
	m_vertexArray.bindAttribute(0, 0, 3, GL_FLOAT, false, 5 * 4, 0);
	m_vertexArray.bindAttribute(0, 1, 3, GL_FLOAT, false, 5 * 4, 3 * 4);

	glViewport(0, 0, width, height);
}

void Scene::update(double delta)
{

}

void Scene::render()
{
	glClearColor(0.0f, 0.0f, 0.0f, 1.0f);
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

	glm::vec3 camPos(0.0f, 1.0f, 3.0f);
	float pitch = -20;
	float yaw = 0;

	glm::mat4 model = glm::translate(glm::vec3(0.0f, -1.0f, 0.0f)) *
					  glm::rotate(glm::radians(90.0f), glm::vec3(1.0f, 0.0f, 0.0f)) * 
					  glm::scale(glm::vec3(10.0f));

	glm::mat4 tMat = glm::translate(-camPos);
	glm::mat4 rMat = glm::inverse(glm::rotate(glm::radians(pitch), glm::vec3(1.0f, 0.0f, 0.0f)) *
								  glm::rotate(glm::radians(yaw), glm::vec3(0.0f, 1.0f, 0.0f)));
	glm::mat4 view = rMat * tMat;

	glm::mat4 proj = glm::perspective(glm::radians(70.0f), (float)1280 / 720, 0.0001f, 1000.0f);
	proj[1][1] *= 1;

	glm::mat4 transform = proj * view * model;

	m_shader.bind();
	m_shader.setUniform("transform", transform);
	m_shader.setUniform("model", model);

	m_vertexArray.bind();
	glDrawArrays(GL_TRIANGLES, 0, 6);
}

void Scene::destroy()
{
	m_vertexArray.destroy();
	m_shader.destroy();
}

Scene* Scene::singleton()
{
	static Scene scene;
	return &scene;
}