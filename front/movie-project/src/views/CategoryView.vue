<template>
  <div v-for="genre in store.genres" :key="genre.id">
    <template v-if="genre.id == genreId">
      <div class="genre-container">
        <div class="char-container">
          <h2>{{ genre.name }}</h2>
        </div>
      </div>
    </template>
  </div>

  <div class="container">
    <!-- container를 container-fluid로 변경 -->
    <div class="row">
      <template v-for="movie in store.movies" :key="movie.id">
        <template v-for="genre in movie.genres" :key="genre.id">
          <template v-if="genre.id == genreId">
            <CategoryMovieCard :movie="movie" />
          </template>
        </template>
      </template>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, watch } from "vue";
import { useMovieStore } from "@/stores/counter";
import { useRoute, RouterLink, onBeforeRouteUpdate } from "vue-router";
import CategoryMovieCard from "@/components/CategoryMovieCard.vue";

const route = useRoute();
const store = useMovieStore();

// 라우터의 장르 파라미터를 감시합니다.
watch(
  () => route.params.genreId,
  (newGenreId) => {
    genreId.value = newGenreId;
  }
);

onMounted(() => {
  store.getGenres();
});

onMounted(() => {
  store.getMovies();
});

const genreId = ref(route.params.genreId);

const beforeRouteUpdate = (to, from, next) => {
  // 컴포넌트가 업데이트되도록 next()를 호출합니다.
  next();
};
</script>

<style scoped>
.genre-container {
  background-color: hsl(10, 8%, 15%);
  align-items: center;
  display: flex;
  padding: auto;
}

.char-container {
  padding: 20px 20px;
  margin-left: 290px;
}
</style>
