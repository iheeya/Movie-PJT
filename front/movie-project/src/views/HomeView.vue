<template>
  <div>
    <div class="carousel-container">
      <Carosel :movies="carouselMovies" />
    </div>
    <div class="container">
      <div class="row">
        <template v-for="movie in store.movies" :key="movie.id">
          <MovieCard :movie="movie" />
        </template>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, watch } from "vue";
import { useMovieStore } from "@/stores/counter";
import MovieCard from "@/components/MovieCard.vue";
import Carosel from "@/components/Carosel.vue";

const store = useMovieStore();
const carouselMovies = ref([]);

const getRandomMovies = (movies, count) => {
  const shuffled = [...movies].sort(() => 0.5 - Math.random());
  return shuffled.slice(0, count);
};

watch(
  () => store.movies,
  (newMovies) => {
    if (newMovies.length) {
      carouselMovies.value = getRandomMovies(newMovies, 5);
    }
  },
  { immediate: true }
);

onMounted(() => {
  store.getMovies();
});
</script>

<style scoped>
.carousel-container {
  /* max-width: 800px; */
  /* width: 80%; */
  margin: auto;

}
</style>
