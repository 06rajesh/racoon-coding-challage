<template>
    <div class="grid">
        <hgroup>
            <h3>{{ upload_file.name }}</h3>
            <h4 v-if="volume > 0">{{ check_volume(volume) }}  mm<sup>3</sup></h4>
            <h4 v-else class="red">{{ check_volume(volume) }}</h4>
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
    volume: number,
}>()

function check_volume(vol: number) {
    if (vol > 0) {
        return vol.toString()
    } else if(vol == 0) {
        return 'Volume could not be calculated'
    } else {
        return 'Invalid File format'
    }
}

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