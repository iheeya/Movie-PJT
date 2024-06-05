<template>
  <div class="movie-card">
    <RouterLink :to="{ name: 'moive-detail', params: { movieId: movie.id } }">
      <img
        :src="`https://image.tmdb.org/t/p/w200/${movie.poster_path}`"
        alt="Movie Poster"
      />
    </RouterLink>
    <div class="content-card">
    <p><i class="fa-solid fa-star" style="color: yellow"></i>  {{ movie.vote_average.toFixed(2) }} <br>
    {{ movie.title }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { RouterLink } from "vue-router";
import { defineProps } from "vue";

defineProps({
  movie: Object,
});
</script>

<style scoped>
.movie-card {
  margin: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  object-fit: cover;
  padding: 0;
  width: 300px;
  height: 450px;
  margin-left: 15px;
  margin-top: 70px;
}

.content-card {
  /* display: flex; */
  justify-content: center;
  /* align-items: center;  */
  text-align: center;
  /* width: 300px;
  height: 70px;
  box-sizing: border-box;
  background-color: #77796d;
  color: black; */
  font-weight: bold;
}

.content {
  text-align: center;
}

img {
  width: 100%; /* 이미지를 부모 요소에 맞게 조정 */
  height: 100%; /* 비율 유지 */
}

img:hover {
  filter: blur(2px); /* 이미지를 흐리게 */
}
</style>
