// Copyright Epic Games, Inc. All Rights Reserved.
/*===========================================================================
	Generated code exported from UnrealHeaderTool.
	DO NOT modify this manually! Edit the corresponding .h files instead!
===========================================================================*/

// IWYU pragma: private, include "BlueprintScreenshotToolTypes.h"
#include "UObject/ObjectMacros.h"
#include "UObject/ScriptMacros.h"

PRAGMA_DISABLE_DEPRECATION_WARNINGS
#ifdef BLUEPRINTSCREENSHOTTOOL_BlueprintScreenshotToolTypes_generated_h
#error "BlueprintScreenshotToolTypes.generated.h already included, missing '#pragma once' in BlueprintScreenshotToolTypes.h"
#endif
#define BLUEPRINTSCREENSHOTTOOL_BlueprintScreenshotToolTypes_generated_h

#define FID_HostProject_Plugins_BlueprintScreenshotTool_Source_BlueprintScreenshotTool_Public_BlueprintScreenshotToolTypes_h_13_GENERATED_BODY \
	friend struct Z_Construct_UScriptStruct_FBSTScreenshotData_Statics; \
	static class UScriptStruct* StaticStruct();


template<> BLUEPRINTSCREENSHOTTOOL_API UScriptStruct* StaticStruct<struct FBSTScreenshotData>();

#undef CURRENT_FILE_ID
#define CURRENT_FILE_ID FID_HostProject_Plugins_BlueprintScreenshotTool_Source_BlueprintScreenshotTool_Public_BlueprintScreenshotToolTypes_h


#define FOREACH_ENUM_EBSTIMAGEFORMAT(op) \
	op(EBSTImageFormat::PNG) \
	op(EBSTImageFormat::JPG) 

enum class EBSTImageFormat : uint8;
template<> struct TIsUEnumClass<EBSTImageFormat> { enum { Value = true }; };
template<> BLUEPRINTSCREENSHOTTOOL_API UEnum* StaticEnum<EBSTImageFormat>();

PRAGMA_ENABLE_DEPRECATION_WARNINGS
