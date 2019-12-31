#version 430 core

layout(location = 0) in vec3 position;
layout(location = 1) in vec2 texCoords;
layout(location = 2) in vec3 normal;

layout(location = 0) out vec2 outTexCoords;
layout(location = 1) out vec3 outWorldPos;
layout(location = 2) out vec3 outNormal;

uniform mat4 transform;
uniform mat4 model;

void main() {
	outTexCoords = texCoords;
	
	mat3 normalMatrix = transpose(inverse(mat3(model)));
	outNormal = normalize(normal * normalMatrix);

	outWorldPos = (model * vec4(position, 1.0)).xyz;
	gl_Position = transform * vec4(position, 1.0);
}