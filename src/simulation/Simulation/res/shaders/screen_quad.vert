#version 430 core

layout(location = 0) in vec3 position;
layout(location = 1) in vec2 texCoords;

layout(location = 0) out vec2 outTexCoords;

uniform mat4 transform;

void main() {
	outTexCoords = texCoords;
	
	gl_Position = transform * vec4(position, 1.0);
}