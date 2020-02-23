#pragma once

#include "Common.h"

class quaternion
{
private:
	glm::vec4 m_base;
public:
	quaternion() : m_base(0.0f, 0.0f, 0.0f, 1.0f) {}
	quaternion(const glm::vec3& base) : m_base(base, 0.0f) {}
	quaternion(const glm::vec4& base) : m_base(base) {}
	quaternion(const glm::vec3& axis, float angle) : m_base(0.0f)
	{
		float sinHalfAngle = std::sin(glm::radians(angle / 2));
		float cosHalfAngle = std::cos(glm::radians(angle / 2));

		m_base.x = axis.x * sinHalfAngle;
		m_base.y = axis.y * sinHalfAngle;
		m_base.z = axis.z * sinHalfAngle;
		m_base.w = cosHalfAngle;
	}
	quaternion(const quaternion& other) { m_base = other.m_base; }

	inline float length() const { return glm::length(m_base); }
	inline quaternion normalize() const { return m_base / length(); }
	inline quaternion conjugate() const { return glm::vec4(-m_base.x, -m_base.y, -m_base.z, m_base.w); }

	inline quaternion mul(const quaternion& other) const
	{
		float newW = (w() * other.w()) - (x() * other.x()) - (y() * other.y()) - (z() * other.z());
		float newX = (x() * other.w()) + (w() * other.x()) + (y() * other.z()) - (z() * other.y());
		float newY = (y() * other.w()) + (w() * other.y()) + (z() * other.x()) - (x() * other.z());
		float newZ = (z() * other.w()) + (w() * other.z()) + (x() * other.y()) - (y() * other.x());

		return quaternion({ newX, newY, newZ, newW });
	}

	inline quaternion mul(const glm::vec3& other) const { return mul(quaternion(glm::vec4(other.x, other.y, other.z, 0.0f))); }

	inline glm::vec3 localRotate(const glm::vec3& localVector) const
	{
		//quaternion rot = mul(localVector).mul(conjugate());
		//return glm::vec3(rot.x(), rot.y(), rot.z());
		return matrix() * localVector;
	}

	inline glm::mat3 matrix() const
	{
		glm::mat3 m;
		m[0][0] = 1.0f - 2.0f * y() * y() - 2.0f * z() * z();
		m[1][0] = 2.0f * x() * y() + 2.0f * w() * z();
		m[2][0] = 2.0f * x() * z() - 2.0f * w() * y();

		m[0][1] = 2.0f * x() * y() - 2.0f * w() * z();
		m[1][1] = 1.0f - 2.0f * x() * x() - 2.0f * z() * z();
		m[2][1] = 2.0f * y() * z() + 2.0f * w() * x();
		
		m[0][2] = 2.0f * x() * z() + 2.0f * w() * y();
		m[1][2] = 2.0f * y() * z() - 2.0f * w() * x();
		m[2][2] = 1.0f - 2.0f * x() * x() - 2.0f * y() * y();

		return m;
	}
	inline glm::mat4 matrix4() const { return glm::mat4(matrix()); }

	inline glm::vec3 forward() const { return localRotate(glm::vec3(0, 0, 1)); }
	inline glm::vec3 right() const { return localRotate(glm::vec3(1, 0, 0)); }
	inline glm::vec3 up() const { return localRotate(glm::vec3(0, 1, 0)); }

	inline quaternion operator+(const quaternion& other) const { return quaternion(m_base + other.m_base); }
	inline quaternion& operator+=(const quaternion& other) { m_base += other.m_base; return *this; }

	inline quaternion operator-(const quaternion& other) const { return quaternion(m_base - other.m_base); }
	inline quaternion& operator-=(const quaternion& other) { m_base -= other.m_base; return *this; }

	inline quaternion operator*(const quaternion& other) const { return mul(other); }
	inline quaternion operator*(const glm::vec3& other) const { return mul(other); }
	inline quaternion& operator*=(const quaternion& other) { return operator=(mul(other)); }

	inline quaternion operator*(float value) const { return quaternion(m_base * value); }
	inline quaternion& operator*=(float value) { m_base *= value; return *this; }

	inline quaternion operator/(float value) const { return quaternion(m_base / value); }
	inline quaternion& operator/=(float value) { m_base /= value; return *this; }

	inline quaternion& operator=(const quaternion& other) { m_base = other.m_base; return *this; }

	inline bool operator==(const quaternion& other) { return m_base == other.m_base; }
	inline bool operator!=(const quaternion& other) { return m_base != other.m_base; }

	inline float& operator[](size_t index) { return m_base[(glm::vec4::length_type)index]; }
	inline const float& operator[](size_t index) const { return m_base[(glm::vec4::length_type)index]; }

	inline float x() const { return m_base.x; }
	inline float y() const { return m_base.y; }
	inline float z() const { return m_base.z; }
	inline float w() const { return m_base.w; }

	inline void x(float x) { m_base.x = x; }
	inline void y(float y) { m_base.y = y; }
	inline void z(float z) { m_base.z = z; }
	inline void w(float w) { m_base.w = w; }
};