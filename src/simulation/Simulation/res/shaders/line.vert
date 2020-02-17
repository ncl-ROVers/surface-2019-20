#version 430 core

layout(location = 0) in vec3 position;
layout(location = 1) in vec3 color;

layout(location = 0) out vec3 outColor;

uniform mat4 transform;

void main() {
	outColor = color;
	
	gl_Position = transform * vec4(position, 1.0);
}