#pragma once

#include <glad/glad.h>
#include <GLFW/glfw3.h>

#include <gtc/matrix_transform.hpp>
#include <gtx/transform.hpp>

#include <gtc/quaternion.hpp>
#include <gtx/quaternion.hpp>
#include <ext/quaternion_trigonometric.hpp>

#include <gtx/rotate_vector.hpp>

#define _CRT_SECURE_NO_WARNINGS

#include <vector>
#include <ostream>
#include <algorithm>
#include <iostream>
#include <cstdint>
#include <filesystem>

#include "io/Logger.h"

typedef uint8_t byte;

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

inline byte* readFileContent(const std::string& path, long int& fileSize)
{
	FILE* file = nullptr;
	errno_t err = 0;
	
	if ((err = fopen_s(&file, path.c_str(), "rb")) != 0)
	{
		char message[2048];
		strerror_s(message, err);

		fprintf(stderr, "Cannot open file %s: %s\n", path.c_str(), message);
		fileSize = 0;

		return nullptr;
	}

	fseek(file, 0, SEEK_END);
	fileSize = ftell(file);

	byte* data = new byte[fileSize];

	fseek(file, 0, SEEK_SET);
	fread(data, fileSize, 1, file);

	fclose(file);

	return data;
}