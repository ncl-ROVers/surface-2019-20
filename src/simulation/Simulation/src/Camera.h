#pragma once

#include "Common.h"

class Camera
{
private:
	glm::vec3 m_position;
	float m_pitch = 0.0f;
	float m_yaw = 0.0f;

	glm::mat4 m_viewMatrix;
	glm::mat4 m_projMatrix;

	bool m_isActive = false;
public:
	Camera();

	void update(double delta);
	void resize(int width, int height);

	glm::vec3 getForward() const;
	glm::vec3 getRight() const;
	glm::vec3 getUp() const;

	inline glm::mat4 getViewMatrix() const { return m_viewMatrix; }
	inline glm::mat4 getProjectionMatrix() const { return m_projMatrix; }

	inline glm::vec3 getPosition() const { return m_position; }
	inline void setPosition(const glm::vec3& position) { m_position = position; }

	inline float getPitch() const { return m_pitch; }
	inline void setPitch(float pitch) { m_pitch = pitch; }

	inline float getYaw() const { return m_yaw; }
	inline void setYaw(float yaw) { m_yaw = yaw; }
};