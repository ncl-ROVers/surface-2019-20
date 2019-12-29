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

	resize(width, height);

	m_camera.setPosition({ 0.0f, 1.0f, 3.0f });
	m_camera.setPitch(-20.0f);
}

void Scene::update(double delta)
{
	m_camera.update(delta);
}

void Scene::render()
{
	glClearColor(1.0f, 0.0f, 0.0f, 1.0f);
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

	glm::mat4 model = glm::translate(glm::vec3(0.0f, -1.0f, 0.0f)) *
					  glm::rotate(glm::radians(90.0f), glm::vec3(1.0f, 0.0f, 0.0f)) * 
					  glm::scale(glm::vec3(10.0f));

	glm::mat4 view = m_camera.getViewMatrix();
	glm::mat4 proj = m_camera.getProjectionMatrix();

	glm::mat4 transform = proj * view * model;

	m_shader.bind();
	m_shader.setUniform("transform", transform);
	m_shader.setUniform("model", model);

	m_vertexArray.bind();
	glDrawArrays(GL_TRIANGLES, 0, 6);
}

void Scene::resize(int width, int height)
{
	glViewport(0, 0, width, height);

	m_camera.resize(width, height);
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