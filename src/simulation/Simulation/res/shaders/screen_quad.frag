#version 430 core

layout(location = 0) in vec2 inTexCoords;

layout(location = 0) out vec4 outColor;

uniform sampler2D target;

void main() {
	outColor = texture(target, inTexCoords);
}