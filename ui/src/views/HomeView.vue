<template>
  <main class="container">
    <h1 class="page-title">Welcome to Racoon</h1>
    <div class="dicoms-list">
      <div class="no-item-text" v-if="all_dicoms.length == 0">No DICOM file uploaded yet. Upload a DICOM file from the upload page.</div>
      <article class="dicoms-list-item grid" v-for="d in all_dicoms">
        <div class="img-container">
          <img :src="d.image" class="dicom-item">
        </div>
        <div class="content">
          <h4>{{ d.name }}</h4>
          <h6>Available Image types: {{ d.imageTypes }}</h6>
          <a :href="d.file" :download="d.name + '.dcm'" role="button">
              Download
          </a>
        </div>
      </article>
    </div>
  </main>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import { reactive, ref } from 'vue'
import axios from "axios";


const http = axios.create({
    headers: {
        "Content-type": "application/json"
    }
});

type DicomsResponse  = {
  file: string
  name: string
  imageTypes: string
  image: string
}

let all_dicoms = ref<DicomsResponse[]>([])


onMounted(() => {
    http.get("/api/dicoms/all")
        .then((resp) => {
          console.log(resp.data)
          all_dicoms.value = resp.data.dicoms as DicomsResponse[]
        })
        .catch((e) => console.log("Could not fetch the Request."))
})

</script>

<style>
.dicom-list-item {
  display: block;
  margin-bottom: 20px;
}
.no-item-text{
  text-align: center;
  font-size: 20px;
  color: gray;
  margin: 100px auto;
}
</style>