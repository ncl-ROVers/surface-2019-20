#pragma once

#include "Common.h"
#include "Rotator.h"

class Transform
{
private:
	glm::vec3 m_position;
	rotator m_rotation;
	glm::vec3 m_scale;
public:
	Transform() : m_position(0.0f), m_rotation(), m_scale(1.0f) {}
	Transform(const Transform& other) : 
		m_position(other.m_position),
		m_rotation(other.m_rotation),
		m_scale(other.m_scale) {}
	
	inline Transform& translateTransform(const glm::vec3& translation) { m_position += translation; return *this; }
	inline Transform& rotateTransform(const rotator& rotation) { m_rotation *= rotation; return *this; }
	inline Transform& scaleTransform(const glm::vec3& scale) { m_scale *= scale; return *this; }

	inline glm::mat4 matrix() const { return glm::translate(m_position) * m_rotation.matrix4() * glm::scale(m_scale); }

	inline const glm::vec3& position() const { return m_position; }
	inline glm::vec3& position() { return m_position; }

	inline const rotator& rotation() const { return m_rotation; }
	inline rotator& rotation() { return m_rotation; }

	inline const glm::vec3& scale() const { return m_scale; }
	inline glm::vec3& scale() { return m_scale; }

	inline void position(const glm::vec3& position) { m_position = position; }
	inline void rotation(const rotator& rotation) { m_rotation = rotation; }
	inline void scale(const glm::vec3& scale) { m_scale = scale; }
};