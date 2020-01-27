#version 430

layout(location = 0) in vec3 position;
layout(location = 1) in vec2 texCoords;

layout(location = 0) out vec2 outTexCorods;
layout(location = 1) out vec3 outNormal;
layout(location = 2) out float outHeight;

uniform mat4 transform;
uniform mat4 model;
uniform double time;

float sine_height(vec2 pos, float angle, float wavelength, float kAmpOverLen, float speed, double time) {
	float freq = 2.0 / wavelength;
	float phaseSpeed = speed * freq;
	vec2 direction = vec2(cos(angle), sin(angle));
	
	return (kAmpOverLen * wavelength) * sin(dot(direction, pos) * freq + float(time) * phaseSpeed);
}

vec2 sine_height_derv(vec2 pos, float angle, float wavelength, float kAmpOverLen, float speed, double time) {
	float freq = 2.0 / wavelength;
	float phaseSpeed = speed * freq;
	vec2 direction = vec2(cos(angle), sin(angle));
	
	float hCos = (kAmpOverLen * wavelength) * cos(dot(direction, pos) * freq + float(time) * phaseSpeed);
	return direction * (freq * hCos);
}

void main() {
	outTexCorods = texCoords;
	
	vec4 wave_info[15];
wave_info[0] = vec4(4.834835330619609, 3.6079053838848276, 0.00409299128715029, 10.915707076869726);
wave_info[1] = vec4(2.0894949001010974, 3.6898520518096865, 0.01540673077101243, 8.228418701410817);
wave_info[2] = vec4(3.2619202304180055, 3.4690197768839988, 0.11955851618874509, 10.026831018184005);
wave_info[3] = vec4(2.9579800716786, 2.6452327868351784, 0.035707526021093804, 10.67431370013531);
wave_info[4] = vec4(1.707782881767083, 2.079499295872217, 0.11731400821929351, 6.310472486343434);
wave_info[5] = vec4(2.677866671405216, 4.8021299541114475, 0.12202940340254324, 8.866530767054034);
wave_info[6] = vec4(0.6927851208993925, 2.64491692074509, 0.0397092308873001, 5.205380047096216);
wave_info[7] = vec4(1.9505235024185041, 5.0347259881382715, 0.12410447417487244, 9.132142404767077);
wave_info[8] = vec4(4.609748286744801, 3.227552538439021, 0.13257989802644418, 10.650967888231728);
wave_info[9] = vec4(4.95349765970807, 4.9316282196759635, 0.030749314038476114, 8.452418591530758);
wave_info[10] = vec4(3.5919611717425295, 2.3592038306049985, 0.09894763497127836, 6.269696213417811);
wave_info[11] = vec4(4.473116031528132, 2.667913039350115, 0.06810425500399925, 10.947817004753972);
wave_info[12] = vec4(4.879871325190958, 5.009150109454495, 0.09233580820170025, 8.804504568310634);
wave_info[13] = vec4(5.9129370530806185, 5.6007637304384525, 0.02473456924560556, 3.5107042734749285);
wave_info[14] = vec4(1.0650536085055478, 5.44341314695237, 0.0942376369105115, 9.803693849470562);

	float offset = 0.0;
	vec2 dH = vec2(0.0);

	float scaleH = 4.0;
	float scaleV = 0.15;
	
	vec3 globalPos = (model * vec4(position, 1.0)).xyz;
	
	for(int i = 0; i < 15; ++i) {
		offset += sine_height(scaleH * globalPos.xz, wave_info[i].x, wave_info[i].y, scaleV * wave_info[i].z, wave_info[i].w, time);
		dH += sine_height_derv(scaleH * globalPos.xz, wave_info[i].x, wave_info[i].y, scaleV * wave_info[i].z, wave_info[i].w, time);
	}
	
	outNormal = normalize(vec3(-dH.x, 1, -dH.y));
	outHeight = 0.5 * offset + 0.5;
	
	gl_Position = transform * vec4(position + vec3(0, offset, 0), 1.0);
}