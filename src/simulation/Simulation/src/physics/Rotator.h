#pragma once

#include "Common.h"

class rotator
{
private:
	glm::vec4 m_base;
public:
	rotator() : m_base(0.0f, 0.0f, 0.0f, 1.0f) {}
	rotator(const glm::vec4& base) : m_base(base) {}
	rotator(const glm::vec3& axis, float angle) : m_base(0.0f)
	{
		float sinHalfAngle = std::sin(glm::radians(angle / 2));
		float cosHalfAngle = std::cos(glm::radians(angle / 2));

		m_base.x = axis.x * sinHalfAngle;
		m_base.y = axis.y * sinHalfAngle;
		m_base.z = axis.z * sinHalfAngle;
		m_base.w = cosHalfAngle;
	}
	rotator(const rotator& other) { m_base = other.m_base; }

	inline float length() const { return glm::length(m_base); }
	inline rotator normalize() const { return m_base / length(); }
	inline rotator conjugate() const { return glm::vec4(-m_base.x, -m_base.y, -m_base.z, m_base.w); }

	inline rotator mul(const rotator& other) const
	{
		float newW = (w() * other.w()) - (x() * other.x()) - (y() * other.y()) - (z() * other.z());
		float newX = (x() * other.w()) + (w() * other.x()) + (y() * other.z()) - (z() * other.y());
		float newY = (y() * other.w()) + (w() * other.y()) + (z() * other.x()) - (x() * other.z());
		float newZ = (z() * other.w()) + (w() * other.z()) + (x() * other.y()) - (y() * other.x());

		return rotator({ newX, newY, newZ, newW });
	}

	inline rotator mul(const glm::vec3& other) const { return mul(rotator(glm::vec4(other.x, other.y, other.z, 0.0f))); }

	inline glm::vec3 localRotate(const glm::vec3& localVector) const
	{
		rotator rot = mul(localVector).mul(conjugate());
		return glm::vec3(rot.x(), rot.y(), rot.z());
	}

	inline glm::mat4 matrix() const { return glm::lookAt(glm::vec3(0.0f), forward(), up());  }

	inline glm::vec3 forward() const { return localRotate(glm::vec3(0, 0, 1)); }
	inline glm::vec3 right() const { return localRotate(glm::vec3(1, 0, 0)); }
	inline glm::vec3 up() const { return localRotate(glm::vec3(0, 1, 0)); }

	inline rotator operator*(const rotator& other) const { return mul(other); }
	inline rotator operator*(const glm::vec3& other) const { return mul(other); }
	inline rotator& operator*=(const rotator& other) { return operator=(mul(other)); }

	inline rotator& operator=(const rotator& other) { m_base = other.m_base; return *this; }

	inline bool operator==(const rotator& other) { return m_base == other.m_base; }
	inline bool operator!=(const rotator& other) { return m_base != other.m_base; }

	inline float operator[](size_t index) const { return m_base[index]; }

	inline float x() const { return m_base.x; }
	inline float y() const { return m_base.y; }
	inline float z() const { return m_base.z; }
	inline float w() const { return m_base.w; }

	inline void x(float x) { m_base.x = x; }
	inline void y(float y) { m_base.y = y; }
	inline void z(float z) { m_base.z = z; }
	inline void w(float w) { m_base.w = w; }
};