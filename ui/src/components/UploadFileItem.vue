<template>
    <div class="grid">
        <hgroup>
            <h3>{{ upload_file.name }}</h3>
            <h4>{{ upload_file.type }}</h4>
        </hgroup>
        <div v-if="submitted" :class="success ? 'status green' : 'status red'">
            <i :class="success ? 'fa-solid fa-check' : 'fa-solid fa-x'"></i>
        </div>
    </div>
</template>

<script setup lang="ts">

// import { ref } from 'vue';

defineProps<{
    upload_file: File,
    submitted: boolean,
    success: boolean,
}>()

</script>

<style scoped>
.status {
    font-size: 45px;
    text-align: right;
    padding-top: 10px;
}

.red {
    color: rgb(238, 64, 46);
}

.green {
    color: rgb(71, 164, 23);
}
</style>