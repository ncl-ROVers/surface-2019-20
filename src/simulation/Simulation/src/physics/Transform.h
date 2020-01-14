#pragma once

#include "Common.h"
#include "Quaternion.h"

class Transform
{
private:
	glm::vec3 m_position = glm::vec3(0.0f);
	quaternion m_rotation = quaternion();
	glm::vec3 m_scale = glm::vec3(1.0f);

	Transform* m_parentTransform = nullptr;
public:
	Transform() : m_position(0.0f), m_rotation(), m_scale(1.0f), m_parentTransform(nullptr) {}
	Transform(const Transform& other) : 
		m_position(other.m_position),
		m_rotation(other.m_rotation),
		m_scale(other.m_scale),
		m_parentTransform(other.m_parentTransform) {}
	
	inline Transform& translateTransform(const glm::vec3& translation) { m_position += translation; return *this; }
	inline Transform& rotateTransform(const quaternion& rotation) { m_rotation *= rotation; return *this; }
	inline Transform& scaleTransform(const glm::vec3& scale) { m_scale *= scale; return *this; }

	inline glm::mat3 rMatrix() const { return !m_parentTransform ? m_rotation.matrix() : (m_parentTransform->rMatrix() * m_rotation.matrix()); }

	inline glm::mat4 localMatrix() const { return glm::translate(m_position) * m_rotation.matrix4() * glm::scale(m_scale); }
	inline glm::mat4 matrix() const { return !m_parentTransform ? localMatrix() : (m_parentTransform->matrix() * localMatrix()); }

	inline const glm::vec3& position() const { return m_position; }
	inline glm::vec3& position() { return m_position; }

	inline const quaternion& rotation() const { return m_rotation; }
	inline quaternion& rotation() { return m_rotation; }

	inline const glm::vec3& scale() const { return m_scale; }
	inline glm::vec3& scale() { return m_scale; }

	inline void position(const glm::vec3& position) { m_position = position; }
	inline void rotation(const quaternion& rotation) { m_rotation = rotation; }
	inline void scale(const glm::vec3& scale) { m_scale = scale; }

	inline void parent(Transform* parent) { m_parentTransform = parent; }
};