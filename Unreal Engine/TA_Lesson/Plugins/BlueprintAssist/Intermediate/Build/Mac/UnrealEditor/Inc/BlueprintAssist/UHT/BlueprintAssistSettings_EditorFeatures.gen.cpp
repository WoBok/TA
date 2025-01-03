// Copyright Epic Games, Inc. All Rights Reserved.
/*===========================================================================
	Generated code exported from UnrealHeaderTool.
	DO NOT modify this manually! Edit the corresponding .h files instead!
===========================================================================*/

#include "UObject/GeneratedCppIncludes.h"
#include "BlueprintAssist/Public/BlueprintAssistSettings_EditorFeatures.h"
#include "Runtime/Slate/Public/Framework/Commands/InputChord.h"
#include "Runtime/SlateCore/Public/Layout/Margin.h"
PRAGMA_DISABLE_DEPRECATION_WARNINGS
void EmptyLinkFunctionForGeneratedCodeBlueprintAssistSettings_EditorFeatures() {}

// Begin Cross Module References
BLUEPRINTASSIST_API UClass* Z_Construct_UClass_UBASettings_EditorFeatures();
BLUEPRINTASSIST_API UClass* Z_Construct_UClass_UBASettings_EditorFeatures_NoRegister();
COREUOBJECT_API UClass* Z_Construct_UClass_UObject();
COREUOBJECT_API UScriptStruct* Z_Construct_UScriptStruct_FLinearColor();
SLATE_API UScriptStruct* Z_Construct_UScriptStruct_FInputChord();
SLATECORE_API UScriptStruct* Z_Construct_UScriptStruct_FMargin();
UPackage* Z_Construct_UPackage__Script_BlueprintAssist();
// End Cross Module References

// Begin Class UBASettings_EditorFeatures
void UBASettings_EditorFeatures::StaticRegisterNativesUBASettings_EditorFeatures()
{
}
IMPLEMENT_CLASS_NO_AUTO_REGISTRATION(UBASettings_EditorFeatures);
UClass* Z_Construct_UClass_UBASettings_EditorFeatures_NoRegister()
{
	return UBASettings_EditorFeatures::StaticClass();
}
struct Z_Construct_UClass_UBASettings_EditorFeatures_Statics
{
#if WITH_METADATA
	static constexpr UECodeGen_Private::FMetaDataPairParam Class_MetaDataParams[] = {
		{ "IncludePath", "BlueprintAssistSettings_EditorFeatures.h" },
		{ "ModuleRelativePath", "Public/BlueprintAssistSettings_EditorFeatures.h" },
		{ "ObjectInitializerConstructorDeclared", "" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_bSetReplicationFlagsAfterRenaming_MetaData[] = {
		{ "Category", "CustomEventReplication" },
		{ "Comment", "/* Set the according replication flags after renaming a custom event by matching the prefixes below */" },
		{ "ModuleRelativePath", "Public/BlueprintAssistSettings_EditorFeatures.h" },
		{ "ToolTip", "Set the according replication flags after renaming a custom event by matching the prefixes below" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_bClearReplicationFlagsWhenRenamingWithNoPrefix_MetaData[] = {
		{ "Category", "CustomEventReplication" },
		{ "Comment", "/* When enabled, renaming a custom event with no matching prefix will apply \"NotReplicated\" */" },
		{ "EditCondition", "bSetReplicationFlagsAfterRenaming" },
		{ "ModuleRelativePath", "Public/BlueprintAssistSettings_EditorFeatures.h" },
		{ "ToolTip", "When enabled, renaming a custom event with no matching prefix will apply \"NotReplicated\"" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_bAddReplicationPrefixToCustomEventTitle_MetaData[] = {
		{ "Category", "CustomEventReplication" },
		{ "Comment", "/* Add the according prefix to the title after changing replication flags */" },
		{ "ModuleRelativePath", "Public/BlueprintAssistSettings_EditorFeatures.h" },
		{ "ToolTip", "Add the according prefix to the title after changing replication flags" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_MulticastPrefix_MetaData[] = {
		{ "Category", "CustomEventReplication" },
		{ "ModuleRelativePath", "Public/BlueprintAssistSettings_EditorFeatures.h" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_ServerPrefix_MetaData[] = {
		{ "Category", "CustomEventReplication" },
		{ "ModuleRelativePath", "Public/BlueprintAssistSettings_EditorFeatures.h" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_ClientPrefix_MetaData[] = {
		{ "Category", "CustomEventReplication" },
		{ "ModuleRelativePath", "Public/BlueprintAssistSettings_EditorFeatures.h" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_bDrawNodeGroupOutline_MetaData[] = {
		{ "Category", "NodeGroup" },
		{ "Comment", "/* Draw an outline to visualise each node group on the graph */" },
		{ "ModuleRelativePath", "Public/BlueprintAssistSettings_EditorFeatures.h" },
		{ "ToolTip", "Draw an outline to visualise each node group on the graph" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_bOnlyDrawGroupOutlineWhenSelected_MetaData[] = {
		{ "Category", "NodeGroup" },
		{ "Comment", "/* Only draw the group outline when selected */" },
		{ "EditCondition", "bDrawNodeGroupOutline" },
		{ "EditConditionHides", "" },
		{ "ModuleRelativePath", "Public/BlueprintAssistSettings_EditorFeatures.h" },
		{ "ToolTip", "Only draw the group outline when selected" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_NodeGroupOutlineColor_MetaData[] = {
		{ "Category", "NodeGroup" },
		{ "Comment", "/* Change the color of the border around the selected pin */" },
		{ "EditCondition", "bDrawNodeGroupOutline" },
		{ "EditConditionHides", "" },
		{ "ModuleRelativePath", "Public/BlueprintAssistSettings_EditorFeatures.h" },
		{ "ToolTip", "Change the color of the border around the selected pin" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_NodeGroupOutlineWidth_MetaData[] = {
		{ "Category", "NodeGroup" },
		{ "Comment", "/* Change the color of the border around the selected pin */" },
		{ "EditCondition", "bDrawNodeGroupOutline" },
		{ "EditConditionHides", "" },
		{ "ModuleRelativePath", "Public/BlueprintAssistSettings_EditorFeatures.h" },
		{ "ToolTip", "Change the color of the border around the selected pin" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_NodeGroupOutlineMargin_MetaData[] = {
		{ "Category", "NodeGroup" },
		{ "Comment", "/* Outline margin around each node */" },
		{ "EditCondition", "bDrawNodeGroupOutline" },
		{ "EditConditionHides", "" },
		{ "ModuleRelativePath", "Public/BlueprintAssistSettings_EditorFeatures.h" },
		{ "ToolTip", "Outline margin around each node" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_bDrawNodeGroupFill_MetaData[] = {
		{ "Category", "NodeGroup" },
		{ "Comment", "/* Draw a fill to show the node groups for selected nodes */" },
		{ "ModuleRelativePath", "Public/BlueprintAssistSettings_EditorFeatures.h" },
		{ "ToolTip", "Draw a fill to show the node groups for selected nodes" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_NodeGroupFillColor_MetaData[] = {
		{ "Category", "NodeGroup" },
		{ "Comment", "/* Change the color of the border around the selected pin */" },
		{ "EditCondition", "bDrawNodeGroupFill" },
		{ "EditConditionHides", "" },
		{ "ModuleRelativePath", "Public/BlueprintAssistSettings_EditorFeatures.h" },
		{ "ToolTip", "Change the color of the border around the selected pin" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_AdditionalDragNodesChords_MetaData[] = {
		{ "Category", "Mouse Features" },
		{ "Comment", "/** Extra input chords to for dragging selected nodes with cursor (same as left-click-dragging) */" },
		{ "ModuleRelativePath", "Public/BlueprintAssistSettings_EditorFeatures.h" },
		{ "ToolTip", "Extra input chords to for dragging selected nodes with cursor (same as left-click-dragging)" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_GroupMovementChords_MetaData[] = {
		{ "Category", "Mouse Features" },
		{ "Comment", "/** Input chords for group dragging (move all linked nodes) */" },
		{ "ModuleRelativePath", "Public/BlueprintAssistSettings_EditorFeatures.h" },
		{ "ToolTip", "Input chords for group dragging (move all linked nodes)" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_LeftSubTreeMovementChords_MetaData[] = {
		{ "Category", "Mouse Features" },
		{ "Comment", "/** Input chords for group dragging (move left linked nodes) */" },
		{ "ModuleRelativePath", "Public/BlueprintAssistSettings_EditorFeatures.h" },
		{ "ToolTip", "Input chords for group dragging (move left linked nodes)" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_RightSubTreeMovementChords_MetaData[] = {
		{ "Category", "Mouse Features" },
		{ "Comment", "/** Input chords for group dragging (move right linked nodes) */" },
		{ "ModuleRelativePath", "Public/BlueprintAssistSettings_EditorFeatures.h" },
		{ "ToolTip", "Input chords for group dragging (move right linked nodes)" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_InsertNewNodeKeyChord_MetaData[] = {
		{ "Category", "General | New Node Behaviour" },
		{ "Comment", "/* Try to insert the node between any current wires when holding down this key */" },
		{ "ModuleRelativePath", "Public/BlueprintAssistSettings_EditorFeatures.h" },
		{ "ToolTip", "Try to insert the node between any current wires when holding down this key" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_bAlwaysConnectExecutionFromParameter_MetaData[] = {
		{ "Category", "General | New Node Behaviour" },
		{ "Comment", "/* When creating a new node from a parameter pin, always try to connect the execution. Holding InsertNewNodeChord will disable this. */" },
		{ "ModuleRelativePath", "Public/BlueprintAssistSettings_EditorFeatures.h" },
		{ "ToolTip", "When creating a new node from a parameter pin, always try to connect the execution. Holding InsertNewNodeChord will disable this." },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_bAlwaysInsertFromParameter_MetaData[] = {
		{ "Category", "General | New Node Behaviour" },
		{ "Comment", "/* When creating a new node from a parameter pin, always try to insert between wires. Holding InsertNewNodeChord will disable this. */" },
		{ "ModuleRelativePath", "Public/BlueprintAssistSettings_EditorFeatures.h" },
		{ "ToolTip", "When creating a new node from a parameter pin, always try to insert between wires. Holding InsertNewNodeChord will disable this." },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_bAlwaysInsertFromExecution_MetaData[] = {
		{ "Category", "General | New Node Behaviour" },
		{ "Comment", "/* When creating a new node from an execution pin, always try to insert between wires. Holding InsertNewNodeChord will disable this. */" },
		{ "ModuleRelativePath", "Public/BlueprintAssistSettings_EditorFeatures.h" },
		{ "ToolTip", "When creating a new node from an execution pin, always try to insert between wires. Holding InsertNewNodeChord will disable this." },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_CopyPinValueChord_MetaData[] = {
		{ "Category", "Inputs" },
		{ "Comment", "/* Copy the pin value to the clipboard */" },
		{ "ModuleRelativePath", "Public/BlueprintAssistSettings_EditorFeatures.h" },
		{ "ToolTip", "Copy the pin value to the clipboard" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_PastePinValueChord_MetaData[] = {
		{ "Category", "Inputs" },
		{ "Comment", "/* Paste the hovered value to the clipboard */" },
		{ "ModuleRelativePath", "Public/BlueprintAssistSettings_EditorFeatures.h" },
		{ "ToolTip", "Paste the hovered value to the clipboard" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_bSelectValuePinWhenCreatingNewNodes_MetaData[] = {
		{ "Category", "Experimental" },
		{ "Comment", "/* Select the first editable parameter pin when a node is created */" },
		{ "ModuleRelativePath", "Public/BlueprintAssistSettings_EditorFeatures.h" },
		{ "ToolTip", "Select the first editable parameter pin when a node is created" },
	};
#endif // WITH_METADATA
	static void NewProp_bSetReplicationFlagsAfterRenaming_SetBit(void* Obj);
	static const UECodeGen_Private::FBoolPropertyParams NewProp_bSetReplicationFlagsAfterRenaming;
	static void NewProp_bClearReplicationFlagsWhenRenamingWithNoPrefix_SetBit(void* Obj);
	static const UECodeGen_Private::FBoolPropertyParams NewProp_bClearReplicationFlagsWhenRenamingWithNoPrefix;
	static void NewProp_bAddReplicationPrefixToCustomEventTitle_SetBit(void* Obj);
	static const UECodeGen_Private::FBoolPropertyParams NewProp_bAddReplicationPrefixToCustomEventTitle;
	static const UECodeGen_Private::FStrPropertyParams NewProp_MulticastPrefix;
	static const UECodeGen_Private::FStrPropertyParams NewProp_ServerPrefix;
	static const UECodeGen_Private::FStrPropertyParams NewProp_ClientPrefix;
	static void NewProp_bDrawNodeGroupOutline_SetBit(void* Obj);
	static const UECodeGen_Private::FBoolPropertyParams NewProp_bDrawNodeGroupOutline;
	static void NewProp_bOnlyDrawGroupOutlineWhenSelected_SetBit(void* Obj);
	static const UECodeGen_Private::FBoolPropertyParams NewProp_bOnlyDrawGroupOutlineWhenSelected;
	static const UECodeGen_Private::FStructPropertyParams NewProp_NodeGroupOutlineColor;
	static const UECodeGen_Private::FFloatPropertyParams NewProp_NodeGroupOutlineWidth;
	static const UECodeGen_Private::FStructPropertyParams NewProp_NodeGroupOutlineMargin;
	static void NewProp_bDrawNodeGroupFill_SetBit(void* Obj);
	static const UECodeGen_Private::FBoolPropertyParams NewProp_bDrawNodeGroupFill;
	static const UECodeGen_Private::FStructPropertyParams NewProp_NodeGroupFillColor;
	static const UECodeGen_Private::FStructPropertyParams NewProp_AdditionalDragNodesChords_Inner;
	static const UECodeGen_Private::FArrayPropertyParams NewProp_AdditionalDragNodesChords;
	static const UECodeGen_Private::FStructPropertyParams NewProp_GroupMovementChords_Inner;
	static const UECodeGen_Private::FArrayPropertyParams NewProp_GroupMovementChords;
	static const UECodeGen_Private::FStructPropertyParams NewProp_LeftSubTreeMovementChords_Inner;
	static const UECodeGen_Private::FArrayPropertyParams NewProp_LeftSubTreeMovementChords;
	static const UECodeGen_Private::FStructPropertyParams NewProp_RightSubTreeMovementChords_Inner;
	static const UECodeGen_Private::FArrayPropertyParams NewProp_RightSubTreeMovementChords;
	static const UECodeGen_Private::FStructPropertyParams NewProp_InsertNewNodeKeyChord;
	static void NewProp_bAlwaysConnectExecutionFromParameter_SetBit(void* Obj);
	static const UECodeGen_Private::FBoolPropertyParams NewProp_bAlwaysConnectExecutionFromParameter;
	static void NewProp_bAlwaysInsertFromParameter_SetBit(void* Obj);
	static const UECodeGen_Private::FBoolPropertyParams NewProp_bAlwaysInsertFromParameter;
	static void NewProp_bAlwaysInsertFromExecution_SetBit(void* Obj);
	static const UECodeGen_Private::FBoolPropertyParams NewProp_bAlwaysInsertFromExecution;
	static const UECodeGen_Private::FStructPropertyParams NewProp_CopyPinValueChord;
	static const UECodeGen_Private::FStructPropertyParams NewProp_PastePinValueChord;
	static void NewProp_bSelectValuePinWhenCreatingNewNodes_SetBit(void* Obj);
	static const UECodeGen_Private::FBoolPropertyParams NewProp_bSelectValuePinWhenCreatingNewNodes;
	static const UECodeGen_Private::FPropertyParamsBase* const PropPointers[];
	static UObject* (*const DependentSingletons[])();
	static constexpr FCppClassTypeInfoStatic StaticCppClassTypeInfo = {
		TCppClassTypeTraits<UBASettings_EditorFeatures>::IsAbstract,
	};
	static const UECodeGen_Private::FClassParams ClassParams;
};
void Z_Construct_UClass_UBASettings_EditorFeatures_Statics::NewProp_bSetReplicationFlagsAfterRenaming_SetBit(void* Obj)
{
	((UBASettings_EditorFeatures*)Obj)->bSetReplicationFlagsAfterRenaming = 1;
}
const UECodeGen_Private::FBoolPropertyParams Z_Construct_UClass_UBASettings_EditorFeatures_Statics::NewProp_bSetReplicationFlagsAfterRenaming = { "bSetReplicationFlagsAfterRenaming", nullptr, (EPropertyFlags)0x0010000000004001, UECodeGen_Private::EPropertyGenFlags::Bool | UECodeGen_Private::EPropertyGenFlags::NativeBool, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, sizeof(bool), sizeof(UBASettings_EditorFeatures), &Z_Construct_UClass_UBASettings_EditorFeatures_Statics::NewProp_bSetReplicationFlagsAfterRenaming_SetBit, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_bSetReplicationFlagsAfterRenaming_MetaData), NewProp_bSetReplicationFlagsAfterRenaming_MetaData) };
void Z_Construct_UClass_UBASettings_EditorFeatures_Statics::NewProp_bClearReplicationFlagsWhenRenamingWithNoPrefix_SetBit(void* Obj)
{
	((UBASettings_EditorFeatures*)Obj)->bClearReplicationFlagsWhenRenamingWithNoPrefix = 1;
}
const UECodeGen_Private::FBoolPropertyParams Z_Construct_UClass_UBASettings_EditorFeatures_Statics::NewProp_bClearReplicationFlagsWhenRenamingWithNoPrefix = { "bClearReplicationFlagsWhenRenamingWithNoPrefix", nullptr, (EPropertyFlags)0x0010000000004001, UECodeGen_Private::EPropertyGenFlags::Bool | UECodeGen_Private::EPropertyGenFlags::NativeBool, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, sizeof(bool), sizeof(UBASettings_EditorFeatures), &Z_Construct_UClass_UBASettings_EditorFeatures_Statics::NewProp_bClearReplicationFlagsWhenRenamingWithNoPrefix_SetBit, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_bClearReplicationFlagsWhenRenamingWithNoPrefix_MetaData), NewProp_bClearReplicationFlagsWhenRenamingWithNoPrefix_MetaData) };
void Z_Construct_UClass_UBASettings_EditorFeatures_Statics::NewProp_bAddReplicationPrefixToCustomEventTitle_SetBit(void* Obj)
{
	((UBASettings_EditorFeatures*)Obj)->bAddReplicationPrefixToCustomEventTitle = 1;
}
const UECodeGen_Private::FBoolPropertyParams Z_Construct_UClass_UBASettings_EditorFeatures_Statics::NewProp_bAddReplicationPrefixToCustomEventTitle = { "bAddReplicationPrefixToCustomEventTitle", nullptr, (EPropertyFlags)0x0010000000004001, UECodeGen_Private::EPropertyGenFlags::Bool | UECodeGen_Private::EPropertyGenFlags::NativeBool, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, sizeof(bool), sizeof(UBASettings_EditorFeatures), &Z_Construct_UClass_UBASettings_EditorFeatures_Statics::NewProp_bAddReplicationPrefixToCustomEventTitle_SetBit, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_bAddReplicationPrefixToCustomEventTitle_MetaData), NewProp_bAddReplicationPrefixToCustomEventTitle_MetaData) };
const UECodeGen_Private::FStrPropertyParams Z_Construct_UClass_UBASettings_EditorFeatures_Statics::NewProp_MulticastPrefix = { "MulticastPrefix", nullptr, (EPropertyFlags)0x0010000000004001, UECodeGen_Private::EPropertyGenFlags::Str, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(UBASettings_EditorFeatures, MulticastPrefix), METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_MulticastPrefix_MetaData), NewProp_MulticastPrefix_MetaData) };
const UECodeGen_Private::FStrPropertyParams Z_Construct_UClass_UBASettings_EditorFeatures_Statics::NewProp_ServerPrefix = { "ServerPrefix", nullptr, (EPropertyFlags)0x0010000000004001, UECodeGen_Private::EPropertyGenFlags::Str, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(UBASettings_EditorFeatures, ServerPrefix), METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_ServerPrefix_MetaData), NewProp_ServerPrefix_MetaData) };
const UECodeGen_Private::FStrPropertyParams Z_Construct_UClass_UBASettings_EditorFeatures_Statics::NewProp_ClientPrefix = { "ClientPrefix", nullptr, (EPropertyFlags)0x0010000000004001, UECodeGen_Private::EPropertyGenFlags::Str, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(UBASettings_EditorFeatures, ClientPrefix), METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_ClientPrefix_MetaData), NewProp_ClientPrefix_MetaData) };
void Z_Construct_UClass_UBASettings_EditorFeatures_Statics::NewProp_bDrawNodeGroupOutline_SetBit(void* Obj)
{
	((UBASettings_EditorFeatures*)Obj)->bDrawNodeGroupOutline = 1;
}
const UECodeGen_Private::FBoolPropertyParams Z_Construct_UClass_UBASettings_EditorFeatures_Statics::NewProp_bDrawNodeGroupOutline = { "bDrawNodeGroupOutline", nullptr, (EPropertyFlags)0x0010000000004001, UECodeGen_Private::EPropertyGenFlags::Bool | UECodeGen_Private::EPropertyGenFlags::NativeBool, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, sizeof(bool), sizeof(UBASettings_EditorFeatures), &Z_Construct_UClass_UBASettings_EditorFeatures_Statics::NewProp_bDrawNodeGroupOutline_SetBit, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_bDrawNodeGroupOutline_MetaData), NewProp_bDrawNodeGroupOutline_MetaData) };
void Z_Construct_UClass_UBASettings_EditorFeatures_Statics::NewProp_bOnlyDrawGroupOutlineWhenSelected_SetBit(void* Obj)
{
	((UBASettings_EditorFeatures*)Obj)->bOnlyDrawGroupOutlineWhenSelected = 1;
}
const UECodeGen_Private::FBoolPropertyParams Z_Construct_UClass_UBASettings_EditorFeatures_Statics::NewProp_bOnlyDrawGroupOutlineWhenSelected = { "bOnlyDrawGroupOutlineWhenSelected", nullptr, (EPropertyFlags)0x0010000000004001, UECodeGen_Private::EPropertyGenFlags::Bool | UECodeGen_Private::EPropertyGenFlags::NativeBool, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, sizeof(bool), sizeof(UBASettings_EditorFeatures), &Z_Construct_UClass_UBASettings_EditorFeatures_Statics::NewProp_bOnlyDrawGroupOutlineWhenSelected_SetBit, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_bOnlyDrawGroupOutlineWhenSelected_MetaData), NewProp_bOnlyDrawGroupOutlineWhenSelected_MetaData) };
const UECodeGen_Private::FStructPropertyParams Z_Construct_UClass_UBASettings_EditorFeatures_Statics::NewProp_NodeGroupOutlineColor = { "NodeGroupOutlineColor", nullptr, (EPropertyFlags)0x0010000000004001, UECodeGen_Private::EPropertyGenFlags::Struct, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(UBASettings_EditorFeatures, NodeGroupOutlineColor), Z_Construct_UScriptStruct_FLinearColor, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_NodeGroupOutlineColor_MetaData), NewProp_NodeGroupOutlineColor_MetaData) };
const UECodeGen_Private::FFloatPropertyParams Z_Construct_UClass_UBASettings_EditorFeatures_Statics::NewProp_NodeGroupOutlineWidth = { "NodeGroupOutlineWidth", nullptr, (EPropertyFlags)0x0010000000004001, UECodeGen_Private::EPropertyGenFlags::Float, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(UBASettings_EditorFeatures, NodeGroupOutlineWidth), METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_NodeGroupOutlineWidth_MetaData), NewProp_NodeGroupOutlineWidth_MetaData) };
const UECodeGen_Private::FStructPropertyParams Z_Construct_UClass_UBASettings_EditorFeatures_Statics::NewProp_NodeGroupOutlineMargin = { "NodeGroupOutlineMargin", nullptr, (EPropertyFlags)0x0010000000004001, UECodeGen_Private::EPropertyGenFlags::Struct, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(UBASettings_EditorFeatures, NodeGroupOutlineMargin), Z_Construct_UScriptStruct_FMargin, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_NodeGroupOutlineMargin_MetaData), NewProp_NodeGroupOutlineMargin_MetaData) }; // 2986890016
void Z_Construct_UClass_UBASettings_EditorFeatures_Statics::NewProp_bDrawNodeGroupFill_SetBit(void* Obj)
{
	((UBASettings_EditorFeatures*)Obj)->bDrawNodeGroupFill = 1;
}
const UECodeGen_Private::FBoolPropertyParams Z_Construct_UClass_UBASettings_EditorFeatures_Statics::NewProp_bDrawNodeGroupFill = { "bDrawNodeGroupFill", nullptr, (EPropertyFlags)0x0010000000000001, UECodeGen_Private::EPropertyGenFlags::Bool | UECodeGen_Private::EPropertyGenFlags::NativeBool, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, sizeof(bool), sizeof(UBASettings_EditorFeatures), &Z_Construct_UClass_UBASettings_EditorFeatures_Statics::NewProp_bDrawNodeGroupFill_SetBit, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_bDrawNodeGroupFill_MetaData), NewProp_bDrawNodeGroupFill_MetaData) };
const UECodeGen_Private::FStructPropertyParams Z_Construct_UClass_UBASettings_EditorFeatures_Statics::NewProp_NodeGroupFillColor = { "NodeGroupFillColor", nullptr, (EPropertyFlags)0x0010000000004001, UECodeGen_Private::EPropertyGenFlags::Struct, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(UBASettings_EditorFeatures, NodeGroupFillColor), Z_Construct_UScriptStruct_FLinearColor, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_NodeGroupFillColor_MetaData), NewProp_NodeGroupFillColor_MetaData) };
const UECodeGen_Private::FStructPropertyParams Z_Construct_UClass_UBASettings_EditorFeatures_Statics::NewProp_AdditionalDragNodesChords_Inner = { "AdditionalDragNodesChords", nullptr, (EPropertyFlags)0x0000000000004000, UECodeGen_Private::EPropertyGenFlags::Struct, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, 0, Z_Construct_UScriptStruct_FInputChord, METADATA_PARAMS(0, nullptr) }; // 4109060215
const UECodeGen_Private::FArrayPropertyParams Z_Construct_UClass_UBASettings_EditorFeatures_Statics::NewProp_AdditionalDragNodesChords = { "AdditionalDragNodesChords", nullptr, (EPropertyFlags)0x0010000000004001, UECodeGen_Private::EPropertyGenFlags::Array, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(UBASettings_EditorFeatures, AdditionalDragNodesChords), EArrayPropertyFlags::None, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_AdditionalDragNodesChords_MetaData), NewProp_AdditionalDragNodesChords_MetaData) }; // 4109060215
const UECodeGen_Private::FStructPropertyParams Z_Construct_UClass_UBASettings_EditorFeatures_Statics::NewProp_GroupMovementChords_Inner = { "GroupMovementChords", nullptr, (EPropertyFlags)0x0000000000004000, UECodeGen_Private::EPropertyGenFlags::Struct, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, 0, Z_Construct_UScriptStruct_FInputChord, METADATA_PARAMS(0, nullptr) }; // 4109060215
const UECodeGen_Private::FArrayPropertyParams Z_Construct_UClass_UBASettings_EditorFeatures_Statics::NewProp_GroupMovementChords = { "GroupMovementChords", nullptr, (EPropertyFlags)0x0010000000004001, UECodeGen_Private::EPropertyGenFlags::Array, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(UBASettings_EditorFeatures, GroupMovementChords), EArrayPropertyFlags::None, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_GroupMovementChords_MetaData), NewProp_GroupMovementChords_MetaData) }; // 4109060215
const UECodeGen_Private::FStructPropertyParams Z_Construct_UClass_UBASettings_EditorFeatures_Statics::NewProp_LeftSubTreeMovementChords_Inner = { "LeftSubTreeMovementChords", nullptr, (EPropertyFlags)0x0000000000004000, UECodeGen_Private::EPropertyGenFlags::Struct, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, 0, Z_Construct_UScriptStruct_FInputChord, METADATA_PARAMS(0, nullptr) }; // 4109060215
const UECodeGen_Private::FArrayPropertyParams Z_Construct_UClass_UBASettings_EditorFeatures_Statics::NewProp_LeftSubTreeMovementChords = { "LeftSubTreeMovementChords", nullptr, (EPropertyFlags)0x0010000000004001, UECodeGen_Private::EPropertyGenFlags::Array, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(UBASettings_EditorFeatures, LeftSubTreeMovementChords), EArrayPropertyFlags::None, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_LeftSubTreeMovementChords_MetaData), NewProp_LeftSubTreeMovementChords_MetaData) }; // 4109060215
const UECodeGen_Private::FStructPropertyParams Z_Construct_UClass_UBASettings_EditorFeatures_Statics::NewProp_RightSubTreeMovementChords_Inner = { "RightSubTreeMovementChords", nullptr, (EPropertyFlags)0x0000000000004000, UECodeGen_Private::EPropertyGenFlags::Struct, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, 0, Z_Construct_UScriptStruct_FInputChord, METADATA_PARAMS(0, nullptr) }; // 4109060215
const UECodeGen_Private::FArrayPropertyParams Z_Construct_UClass_UBASettings_EditorFeatures_Statics::NewProp_RightSubTreeMovementChords = { "RightSubTreeMovementChords", nullptr, (EPropertyFlags)0x0010000000004001, UECodeGen_Private::EPropertyGenFlags::Array, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(UBASettings_EditorFeatures, RightSubTreeMovementChords), EArrayPropertyFlags::None, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_RightSubTreeMovementChords_MetaData), NewProp_RightSubTreeMovementChords_MetaData) }; // 4109060215
const UECodeGen_Private::FStructPropertyParams Z_Construct_UClass_UBASettings_EditorFeatures_Statics::NewProp_InsertNewNodeKeyChord = { "InsertNewNodeKeyChord", nullptr, (EPropertyFlags)0x0010000000004001, UECodeGen_Private::EPropertyGenFlags::Struct, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(UBASettings_EditorFeatures, InsertNewNodeKeyChord), Z_Construct_UScriptStruct_FInputChord, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_InsertNewNodeKeyChord_MetaData), NewProp_InsertNewNodeKeyChord_MetaData) }; // 4109060215
void Z_Construct_UClass_UBASettings_EditorFeatures_Statics::NewProp_bAlwaysConnectExecutionFromParameter_SetBit(void* Obj)
{
	((UBASettings_EditorFeatures*)Obj)->bAlwaysConnectExecutionFromParameter = 1;
}
const UECodeGen_Private::FBoolPropertyParams Z_Construct_UClass_UBASettings_EditorFeatures_Statics::NewProp_bAlwaysConnectExecutionFromParameter = { "bAlwaysConnectExecutionFromParameter", nullptr, (EPropertyFlags)0x0010000000004001, UECodeGen_Private::EPropertyGenFlags::Bool | UECodeGen_Private::EPropertyGenFlags::NativeBool, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, sizeof(bool), sizeof(UBASettings_EditorFeatures), &Z_Construct_UClass_UBASettings_EditorFeatures_Statics::NewProp_bAlwaysConnectExecutionFromParameter_SetBit, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_bAlwaysConnectExecutionFromParameter_MetaData), NewProp_bAlwaysConnectExecutionFromParameter_MetaData) };
void Z_Construct_UClass_UBASettings_EditorFeatures_Statics::NewProp_bAlwaysInsertFromParameter_SetBit(void* Obj)
{
	((UBASettings_EditorFeatures*)Obj)->bAlwaysInsertFromParameter = 1;
}
const UECodeGen_Private::FBoolPropertyParams Z_Construct_UClass_UBASettings_EditorFeatures_Statics::NewProp_bAlwaysInsertFromParameter = { "bAlwaysInsertFromParameter", nullptr, (EPropertyFlags)0x0010000000004001, UECodeGen_Private::EPropertyGenFlags::Bool | UECodeGen_Private::EPropertyGenFlags::NativeBool, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, sizeof(bool), sizeof(UBASettings_EditorFeatures), &Z_Construct_UClass_UBASettings_EditorFeatures_Statics::NewProp_bAlwaysInsertFromParameter_SetBit, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_bAlwaysInsertFromParameter_MetaData), NewProp_bAlwaysInsertFromParameter_MetaData) };
void Z_Construct_UClass_UBASettings_EditorFeatures_Statics::NewProp_bAlwaysInsertFromExecution_SetBit(void* Obj)
{
	((UBASettings_EditorFeatures*)Obj)->bAlwaysInsertFromExecution = 1;
}
const UECodeGen_Private::FBoolPropertyParams Z_Construct_UClass_UBASettings_EditorFeatures_Statics::NewProp_bAlwaysInsertFromExecution = { "bAlwaysInsertFromExecution", nullptr, (EPropertyFlags)0x0010000000004001, UECodeGen_Private::EPropertyGenFlags::Bool | UECodeGen_Private::EPropertyGenFlags::NativeBool, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, sizeof(bool), sizeof(UBASettings_EditorFeatures), &Z_Construct_UClass_UBASettings_EditorFeatures_Statics::NewProp_bAlwaysInsertFromExecution_SetBit, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_bAlwaysInsertFromExecution_MetaData), NewProp_bAlwaysInsertFromExecution_MetaData) };
const UECodeGen_Private::FStructPropertyParams Z_Construct_UClass_UBASettings_EditorFeatures_Statics::NewProp_CopyPinValueChord = { "CopyPinValueChord", nullptr, (EPropertyFlags)0x0010000000004001, UECodeGen_Private::EPropertyGenFlags::Struct, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(UBASettings_EditorFeatures, CopyPinValueChord), Z_Construct_UScriptStruct_FInputChord, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_CopyPinValueChord_MetaData), NewProp_CopyPinValueChord_MetaData) }; // 4109060215
const UECodeGen_Private::FStructPropertyParams Z_Construct_UClass_UBASettings_EditorFeatures_Statics::NewProp_PastePinValueChord = { "PastePinValueChord", nullptr, (EPropertyFlags)0x0010000000004001, UECodeGen_Private::EPropertyGenFlags::Struct, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(UBASettings_EditorFeatures, PastePinValueChord), Z_Construct_UScriptStruct_FInputChord, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_PastePinValueChord_MetaData), NewProp_PastePinValueChord_MetaData) }; // 4109060215
void Z_Construct_UClass_UBASettings_EditorFeatures_Statics::NewProp_bSelectValuePinWhenCreatingNewNodes_SetBit(void* Obj)
{
	((UBASettings_EditorFeatures*)Obj)->bSelectValuePinWhenCreatingNewNodes = 1;
}
const UECodeGen_Private::FBoolPropertyParams Z_Construct_UClass_UBASettings_EditorFeatures_Statics::NewProp_bSelectValuePinWhenCreatingNewNodes = { "bSelectValuePinWhenCreatingNewNodes", nullptr, (EPropertyFlags)0x0010000000004001, UECodeGen_Private::EPropertyGenFlags::Bool | UECodeGen_Private::EPropertyGenFlags::NativeBool, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, sizeof(bool), sizeof(UBASettings_EditorFeatures), &Z_Construct_UClass_UBASettings_EditorFeatures_Statics::NewProp_bSelectValuePinWhenCreatingNewNodes_SetBit, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_bSelectValuePinWhenCreatingNewNodes_MetaData), NewProp_bSelectValuePinWhenCreatingNewNodes_MetaData) };
const UECodeGen_Private::FPropertyParamsBase* const Z_Construct_UClass_UBASettings_EditorFeatures_Statics::PropPointers[] = {
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_UBASettings_EditorFeatures_Statics::NewProp_bSetReplicationFlagsAfterRenaming,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_UBASettings_EditorFeatures_Statics::NewProp_bClearReplicationFlagsWhenRenamingWithNoPrefix,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_UBASettings_EditorFeatures_Statics::NewProp_bAddReplicationPrefixToCustomEventTitle,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_UBASettings_EditorFeatures_Statics::NewProp_MulticastPrefix,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_UBASettings_EditorFeatures_Statics::NewProp_ServerPrefix,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_UBASettings_EditorFeatures_Statics::NewProp_ClientPrefix,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_UBASettings_EditorFeatures_Statics::NewProp_bDrawNodeGroupOutline,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_UBASettings_EditorFeatures_Statics::NewProp_bOnlyDrawGroupOutlineWhenSelected,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_UBASettings_EditorFeatures_Statics::NewProp_NodeGroupOutlineColor,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_UBASettings_EditorFeatures_Statics::NewProp_NodeGroupOutlineWidth,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_UBASettings_EditorFeatures_Statics::NewProp_NodeGroupOutlineMargin,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_UBASettings_EditorFeatures_Statics::NewProp_bDrawNodeGroupFill,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_UBASettings_EditorFeatures_Statics::NewProp_NodeGroupFillColor,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_UBASettings_EditorFeatures_Statics::NewProp_AdditionalDragNodesChords_Inner,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_UBASettings_EditorFeatures_Statics::NewProp_AdditionalDragNodesChords,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_UBASettings_EditorFeatures_Statics::NewProp_GroupMovementChords_Inner,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_UBASettings_EditorFeatures_Statics::NewProp_GroupMovementChords,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_UBASettings_EditorFeatures_Statics::NewProp_LeftSubTreeMovementChords_Inner,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_UBASettings_EditorFeatures_Statics::NewProp_LeftSubTreeMovementChords,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_UBASettings_EditorFeatures_Statics::NewProp_RightSubTreeMovementChords_Inner,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_UBASettings_EditorFeatures_Statics::NewProp_RightSubTreeMovementChords,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_UBASettings_EditorFeatures_Statics::NewProp_InsertNewNodeKeyChord,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_UBASettings_EditorFeatures_Statics::NewProp_bAlwaysConnectExecutionFromParameter,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_UBASettings_EditorFeatures_Statics::NewProp_bAlwaysInsertFromParameter,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_UBASettings_EditorFeatures_Statics::NewProp_bAlwaysInsertFromExecution,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_UBASettings_EditorFeatures_Statics::NewProp_CopyPinValueChord,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_UBASettings_EditorFeatures_Statics::NewProp_PastePinValueChord,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_UBASettings_EditorFeatures_Statics::NewProp_bSelectValuePinWhenCreatingNewNodes,
};
static_assert(UE_ARRAY_COUNT(Z_Construct_UClass_UBASettings_EditorFeatures_Statics::PropPointers) < 2048);
UObject* (*const Z_Construct_UClass_UBASettings_EditorFeatures_Statics::DependentSingletons[])() = {
	(UObject* (*)())Z_Construct_UClass_UObject,
	(UObject* (*)())Z_Construct_UPackage__Script_BlueprintAssist,
};
static_assert(UE_ARRAY_COUNT(Z_Construct_UClass_UBASettings_EditorFeatures_Statics::DependentSingletons) < 16);
const UECodeGen_Private::FClassParams Z_Construct_UClass_UBASettings_EditorFeatures_Statics::ClassParams = {
	&UBASettings_EditorFeatures::StaticClass,
	"EditorPerProjectUserSettings",
	&StaticCppClassTypeInfo,
	DependentSingletons,
	nullptr,
	Z_Construct_UClass_UBASettings_EditorFeatures_Statics::PropPointers,
	nullptr,
	UE_ARRAY_COUNT(DependentSingletons),
	0,
	UE_ARRAY_COUNT(Z_Construct_UClass_UBASettings_EditorFeatures_Statics::PropPointers),
	0,
	0x001000A4u,
	METADATA_PARAMS(UE_ARRAY_COUNT(Z_Construct_UClass_UBASettings_EditorFeatures_Statics::Class_MetaDataParams), Z_Construct_UClass_UBASettings_EditorFeatures_Statics::Class_MetaDataParams)
};
UClass* Z_Construct_UClass_UBASettings_EditorFeatures()
{
	if (!Z_Registration_Info_UClass_UBASettings_EditorFeatures.OuterSingleton)
	{
		UECodeGen_Private::ConstructUClass(Z_Registration_Info_UClass_UBASettings_EditorFeatures.OuterSingleton, Z_Construct_UClass_UBASettings_EditorFeatures_Statics::ClassParams);
	}
	return Z_Registration_Info_UClass_UBASettings_EditorFeatures.OuterSingleton;
}
template<> BLUEPRINTASSIST_API UClass* StaticClass<UBASettings_EditorFeatures>()
{
	return UBASettings_EditorFeatures::StaticClass();
}
DEFINE_VTABLE_PTR_HELPER_CTOR(UBASettings_EditorFeatures);
UBASettings_EditorFeatures::~UBASettings_EditorFeatures() {}
// End Class UBASettings_EditorFeatures

// Begin Registration
struct Z_CompiledInDeferFile_FID_Build_U5M_Marketplace_Mac_Sync_LocalBuilds_PluginTemp_HostProject_Plugins_BlueprintAssist_Source_BlueprintAssist_Public_BlueprintAssistSettings_EditorFeatures_h_Statics
{
	static constexpr FClassRegisterCompiledInInfo ClassInfo[] = {
		{ Z_Construct_UClass_UBASettings_EditorFeatures, UBASettings_EditorFeatures::StaticClass, TEXT("UBASettings_EditorFeatures"), &Z_Registration_Info_UClass_UBASettings_EditorFeatures, CONSTRUCT_RELOAD_VERSION_INFO(FClassReloadVersionInfo, sizeof(UBASettings_EditorFeatures), 285779491U) },
	};
};
static FRegisterCompiledInInfo Z_CompiledInDeferFile_FID_Build_U5M_Marketplace_Mac_Sync_LocalBuilds_PluginTemp_HostProject_Plugins_BlueprintAssist_Source_BlueprintAssist_Public_BlueprintAssistSettings_EditorFeatures_h_3873390955(TEXT("/Script/BlueprintAssist"),
	Z_CompiledInDeferFile_FID_Build_U5M_Marketplace_Mac_Sync_LocalBuilds_PluginTemp_HostProject_Plugins_BlueprintAssist_Source_BlueprintAssist_Public_BlueprintAssistSettings_EditorFeatures_h_Statics::ClassInfo, UE_ARRAY_COUNT(Z_CompiledInDeferFile_FID_Build_U5M_Marketplace_Mac_Sync_LocalBuilds_PluginTemp_HostProject_Plugins_BlueprintAssist_Source_BlueprintAssist_Public_BlueprintAssistSettings_EditorFeatures_h_Statics::ClassInfo),
	nullptr, 0,
	nullptr, 0);
// End Registration
PRAGMA_ENABLE_DEPRECATION_WARNINGS
