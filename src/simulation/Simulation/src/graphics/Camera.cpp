#include "Camera.h"

#include "Input.h"

Camera::Camera() :
	m_position(0.0f), m_pitch(0.0f), m_yaw(0.0f), m_isActive(false)
{
}

void Camera::update(double delta)
{
	const float moveSpeed = 5.0f;
	const float lookSpeed = 12.0f;

	//Movement control
	if (m_isActive && m_moveEnabled)
	{
		if (Input::isKeyDown(GLFW_KEY_W))
		{
			m_position += getForward() * (float)(moveSpeed * delta);
		}

		if (Input::isKeyDown(GLFW_KEY_S))
		{
			m_position -= getForward() * (float)(moveSpeed * delta);
		}

		if (Input::isKeyDown(GLFW_KEY_A))
		{
			m_position -= getRight() * (float)(moveSpeed * delta);
		}

		if (Input::isKeyDown(GLFW_KEY_D))
		{
			m_position += getRight() * (float)(moveSpeed * delta);
		}

		if (Input::isKeyDown(GLFW_KEY_SPACE))
		{
			m_position.y += (float)(moveSpeed * delta);
		}

		if (Input::isKeyDown(GLFW_KEY_LEFT_SHIFT))
		{
			m_position.y -= (float)(moveSpeed * delta);
		}
	}

	if (Input::isKeyPressed(GLFW_KEY_ESCAPE))
	{
		m_isActive = !m_isActive;

		Input::setMouseVisible(!m_isActive);
		
		if (m_isActive)
		{
			Input::setMousePos(Input::getWindowSize() / 2.0f);
		}
	}

	//Orientation control
	if (m_isActive && m_lookEnabled)
	{
		glm::vec2 centerOffset = Input::getMousePos() - Input::getWindowSize() / 2.0f;
		m_yaw -= centerOffset.x * (float)(lookSpeed * delta);
		m_pitch -= centerOffset.y * (float)(lookSpeed * delta);

		m_pitch = std::clamp(m_pitch, -80.0f, 80.0f);
		m_yaw = std::fmod(m_yaw, 360.0f);

		Input::setMousePos(Input::getWindowSize() / 2.0f);
	}

	//Calculate new view matrix
	glm::mat4 tMat = glm::translate(-m_position);
	glm::mat4 rMat = glm::inverse(glm::rotate(glm::radians(m_yaw), glm::vec3(0.0f, 1.0f, 0.0f)) *
								  glm::rotate(glm::radians(m_pitch), glm::vec3(1.0f, 0.0f, 0.0f)));
	
	m_viewMatrix = rMat * tMat;
}

void Camera::resize(int width, int height)
{
	m_projMatrix = glm::perspective(glm::radians(m_fov), (float)width / height, 0.01f, 1000.0f);
}

void Camera::fromSettings(const CameraSettings& settings)
{
	m_position = settings.position;
	m_pitch = settings.pitch;
	m_yaw = settings.yaw;
	m_fov = settings.fov;

	m_moveEnabled = settings.allowMovement;
	m_lookEnabled = settings.allowLooking;
}

glm::vec3 Camera::getForward() const
{
	return polarToCartesian(m_pitch, m_yaw);
}

glm::vec3 Camera::getRight() const
{
	return polarToCartesian(0, m_yaw - 90.0f);
}

glm::vec3 Camera::getUp() const
{
	return polarToCartesian(m_pitch - 90.0f, m_yaw);
}
