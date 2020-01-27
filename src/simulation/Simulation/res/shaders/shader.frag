#version 430 core

layout(location = 0) in vec2 inTexCoords;
layout(location = 1) in vec3 inWorldPos;
layout(location = 2) in vec3 inNormal;

layout(location = 0) out vec4 outColor;

uniform sampler2D albedo;
uniform vec3 sunDirection;
uniform vec3 ambientLighting;

void main() {
	float directLightAmount = max(dot(inNormal, -sunDirection), 0);
	
	vec3 lighting = vec3(directLightAmount);//vec3(directLightAmount) + ambientLighting;
	
	outColor = vec4(texture(albedo, inTexCoords).xyz * lighting, 1.0);
}