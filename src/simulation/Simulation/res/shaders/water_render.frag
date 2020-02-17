#version 430

layout(location = 0) in vec2 inTexCoords;
layout(location = 1) in vec3 inNormal;
layout(location = 2) in float inHeight;

layout(location = 0) out vec4 outColor;

void main() {
//	float lighting = max(dot(inNormal, vec3(0, 1, 0)), 0.0);
//	outColor = vec4(vec3(lighting), 1.0);
	outColor = vec4(inHeight, 0.6, 1.0, 1.0);
}