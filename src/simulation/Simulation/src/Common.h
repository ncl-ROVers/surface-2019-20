#pragma once

#include <glad/glad.h>
#include <GLFW/glfw3.h>

#include <gtc/matrix_transform.hpp>
#include <gtx/transform.hpp>

#include <gtc/quaternion.hpp>
#include <gtx/quaternion.hpp>
#include <ext/quaternion_trigonometric.hpp>

#include <gtx/rotate_vector.hpp>

#include <vector>
#include <ostream>
#include <algorithm>
#include <iostream>

template<int D, typename T, glm::qualifier Q>
inline std::ostream& operator<<(std::ostream& os, const glm::vec<D, T, Q>& value)
{
	os << "(";
	for (int i = 0; i < D - 1; ++i)
	{
		os << value[i] << ", ";
	}
	os << value[D - 1] << ")";

	return os;
}

inline glm::vec3 polarToCartesian(float xRot, float yRot)
{
	float x = -std::sin(glm::radians(yRot)) * std::cos(glm::radians(xRot));
	float y = std::sin(glm::radians(xRot));
	float z = -std::cos(glm::radians(yRot)) * std::cos(glm::radians(xRot));

	return { x, y, z };
}