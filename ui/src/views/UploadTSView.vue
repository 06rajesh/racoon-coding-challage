<template>
    <div class="container">
        <h1 class="page-title">Upload a DICOM File</h1>
        <article>
            <div class="grid place-items-cented nx-auto h-96">
                <FileUpload class="w-72 h72" @upload="startFileUpload" />
            </div>
        </article>
        <div class="upload-list" v-for="(item, idx) in upload_list" :key="item.name + '_' + idx">
            <UploadFileItem :upload_file="item" :submitted="submitted" :success="file_status[idx]"/>
        </div>
        <div class="grid">
            <button :disabled="upload_list.length == 0" class="warning" @click="clearUploadList">
                <i class="fa-solid fa-trash"></i> Clear All
            </button>
            <button :disabled="upload_list.length == 0" @click="handleUploadButton">
                <i class="fa-solid fa-upload"></i> Upload
            </button>
        </div>        
    </div>
</template>

<script setup lang="ts">
import { onMounted, defineAsyncComponent } from 'vue';
import { reactive, ref } from 'vue'
import axios from "axios";
import UploadFileItem from '@/components/UploadFileItem.vue';

const FileUpload = defineAsyncComponent(() => import('../components/FileUpload.vue'))

var upload_list: File[] = reactive([])
var file_status: boolean[] = reactive([])
var submitted = ref(false)

const http = axios.create({
    headers: {
        "Content-type": "application/json"
    }
});


onMounted(() => {
    http.get("/api")
        .then((resp) => console.log("Connection to API established"))
        .catch((e) => console.log("Could not fetch the Request."))
})

function uploadFileToApi(file: File): Promise<boolean> {
    return new Promise((resolve, reject) => {
        var formData = new FormData();
        formData.append("file", file);
        axios.post(
            '/api/upload/',
            formData,
            {
                headers: {
                    'accept': 'application/json',
                    'Content-Type': 'multipart/form-data'
                }
            })
            .then((resp) => {
                if ((resp.data) && (resp.data.status == 'success')){
                    resolve(true)
                }
                resolve(false)
            })
            .catch((e) => {
                reject(e)
            })
    })
    
}

async function handleUploadButton(){
    for(let i=0; i<upload_list.length; i++){
        var resp = await uploadFileToApi(upload_list[i])
        file_status[i] = resp
    }

    submitted.value = true
}

function clearUploadList() {
    upload_list.splice(0)
    file_status.splice(0)
}

function startFileUpload(files: File[]) {
    upload_list.push.apply(upload_list, files)
    files.forEach((f) => {
        file_status.push(false)
    })
}
</script>

<style scoped></style>