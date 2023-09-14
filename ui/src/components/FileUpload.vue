<template>
    <label v-bind="$attrs" class="label" 
        :class="entering ? 'bg-gray-500' : 'bg-gray-100'" @drop.prevent="handleDrop"
        @dragenter="entering=true" @dragleave="entering=false"
    >
        <input multiple type="file" class="input" @input="handleInput">
        <span class="message">
            Drop your files here or click here to upload your file.<br>
            <span class="error" v-if="errormsg != ''">{{ errormsg }}</span>
        </span>
       
    </label>
</template>

<script setup lang="ts">
import {onMounted, onUnmounted, ref} from "vue"

const events = ["dragenter", "dragleave", "dragover", "drop"]
let errormsg = ref<string>('')

onMounted(()=>{
    events.forEach(event => document.body.addEventListener(event, (e)=>e.preventDefault()))
})

onUnmounted(()=>{
    events.forEach(event => document.body.removeEventListener(event, (e)=>e.preventDefault()))
})

const emit = defineEmits<{(e:"upload", files: File[]):void}>()

const entering = ref(false)

function handleDragEnter(e: DragEvent): void {
    console.log("Entering Drag Event")
    if (e.dataTransfer) {
        e.dataTransfer.effectAllowed = 'all'
        e.dataTransfer.dropEffect = 'move'
    }
    console.log(e.dataTransfer)
}

function handleDrop(e : DragEvent) : void {
    // console.log('Handling Drop')
    if (e.dataTransfer && e.dataTransfer.files.length == 0) {
        errormsg.value = 'No file found from the drag event. Please try dragging the files again or click here to select the file from the popup.'
    }
    const files = e.dataTransfer?.files as FileList
    emit("upload", [...files])
}

function handleInput(e : Event) : void {
    // console.log('Handling Input')
    const files = (e.target as HTMLInputElement).files as FileList
    emit("upload", [...files])
}

</script>

<style scoped lang="css">
.label {
    position: relative;
    transition: all 3s ease-in-out;
    border: 1px solid  rgb(107 114 128);
    min-height: 250px;
    padding: 15px;
}
.input {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    visibility: hidden;
}
.message {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    text-align: center;
    font-size: 22px;
}

.error{
    color: red;
    font-size: 16px;
}

.bg-gray-100 {
    background-color: rgb(243 244 246);
}

.bg-gray-500 {
    background-color: rgb(107 114 128);
}
</style>