<template>
  <div>
    <!-- 이미지 사전로드를 위한 숨겨진 요소 -->
    <div style="display: none;">
      <img v-for="movie in movies" :key="movie.id" :src="`https://image.tmdb.org/t/p/w500/${movie.poster_path}`" alt="Preload Image">
    </div>

    <!-- 카로셀 -->
    <div id="carouselExampleCaptions" class="carousel slide c" data-bs-ride="carousel" data-bs-interval="4000"> <!-- 5초 간격으로 설정 -->
      <div class="carousel-indicators">
        <button v-for="(movie, index) in movies" :key="index" :data-bs-target="'#carouselExampleCaptions'" :data-bs-slide-to="index" :class="{ active: index === 0 }" :aria-current="index === 0 ? 'true' : undefined" :aria-label="'Slide ' + (index + 1)"></button>
      </div>

      <div class="carousel-inner">
        <div v-for="(movie, index) in movies" :key="movie.id" :class="['carousel-item', { active: index === 0 }]">
          <div class="d-flex align-items-center">
            <div class="w-50 pe-3">
              <RouterLink :to="{name:'moive-detail', params:{movieId:movie.id}}">
              <img :src="`https://image.tmdb.org/t/p/w500/${movie.poster_path}`" class="d-block w-100" :alt="movie.title"> 
            </RouterLink>
            </div>
            <div class="w-100">
              <div>
                <h5>{{ movie.title }}</h5>
                <br>
                <p>
                  {{ truncatedOverview(movie.overview) }}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <button class="carousel-control-prev" type="button" data-bs-target="#carouselExampleCaptions" data-bs-slide="prev">
        <span class="carousel-control-prev-icon" aria-hidden="true"></span>
        <span class="visually-hidden">Previous</span>
      </button>
      <button class="carousel-control-next" type="button" data-bs-target="#carouselExampleCaptions" data-bs-slide="next">
        <span class="carousel-control-next-icon" aria-hidden="true"></span>
        <span class="visually-hidden">Next</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from "vue";
import { RouterLink } from "vue-router";

const props = defineProps({
  movies: Array
});

const truncatedOverview = (overview) => {
  if (overview.length > 300) {
    return overview.slice(0, 300) + '...';
  }
  return overview;
};
</script>

<style scoped>
.carousel-inner {
  max-height: 300px;
  width: 80%
}
.carousel-item img {
  max-height: 300px;
  object-fit: contain;
  margin-right: 10px;
}

.c {
  margin: 50px 200px;
}
</style>
