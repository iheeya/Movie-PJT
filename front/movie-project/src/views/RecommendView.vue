<template>
  <div>
    <br>    
    <!-- 좋아요 한 영화가 존재하지 않을 경우 -->
    <template v-if="warn == '좋아하는 영화를 골라주세요!'">
      <div class="title">
        <h3>{{ store.name }}님, 좋아하는 영화가 아직 없으시네요.</h3>
        <h3>{{ warn }}</h3> 
      </div>

      <div class="container">
        <div class="row">
          <template v-for="(movie, index) in store.movies" :key="movie.id">
            <div class="col-lg-3">
              <MovieCard :movie="movie" />
              <br>
              <button @click="toggleLike(movie)" class="btn btn-lg like" v-if="store.isLogin">
                <i v-if="likeStatuses[movie.id]" class="fa-solid fa-heart" style="color: #ff0000"></i>
                <i v-else class="fa-regular fa-heart" style="color: #ff0000"></i>
              </button>
            </div>
            <!-- Add a new row after every 4 movies or if it's the last movie -->
            <template v-if="(index + 1) % 4 === 0 || index === store.movies.length - 1">
            </template>
          </template>
        </div>
      </div>
      <button class="scroll-to-top btn btn-link" @click="redirectToRecommendMovies">영화 추천받기</button>
    </template>
   
    <!-- 좋아요 한 영화가 존재할 경우 -->
    <h2 class="title">{{ store.name }}님에게 추천하는 영화목록</h2>
    <div class="container">
        <div class="row">
          <template v-for="movie in recommendedMovies" :key="movie.id">
            <div class="col-lg-3">
              <MovieCard :movie="movie" />
              <br>
              
            </div>
            <!-- Add a new row after every 4 movies or if it's the last movie -->
            <template v-if="(index + 1) % 4 === 0 || index === store.movies.length - 1">
            </template>
          </template>
        </div>
      </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { useMovieStore } from "@/stores/counter";
import MovieCard from '@/components/MovieCard.vue';

const store = useMovieStore();
const recommendedMovies = ref([]);
const warn = ref("");
const likeStatuses = ref({}); // 각 영화의 좋아요 상태를 저장할 객체
const router = useRouter()
const fetchRecommendedMovies = () => {
  axios({
    method: "get",
    url: `${store.API_URL}/accounts/recommendations/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then((response) => {
      if (response.data.length === 0) {
        console.warn("No recommended movies found.");
        warn.value = "좋아하는 영화를 골라주세요!";
      }
      recommendedMovies.value = response.data; // 추천 영화 목록을 업데이트
      fetchAllLikeStatuses(); // 각 영화의 좋아요 상태를 가져옴
    })
    .catch((error) => {
      console.error("Error fetching recommended movies: ", error);
    });
};

const fetchAllLikeStatuses = () => {
  recommendedMovies.value.forEach(movie => {
    fetchLikeStatus(movie);
  });
};

const fetchLikeStatus = (movie) => {
  axios({
    method: "get",
    url: `${store.API_URL}/accounts/movies/${movie.id}/like-status/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then((response) => {
      likeStatuses.value = { ...likeStatuses.value, [movie.id]: response.data.is_liked };
    })
    .catch((error) => {
      console.error("Error fetching like status: ", error);
    });
};

const toggleLike = (movie) => {
  axios({
    method: "post",
    url: `${store.API_URL}/accounts/movies/${movie.id}/toggle-like/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then((response) => {
      likeStatuses.value = { ...likeStatuses.value, [movie.id]: response.data.is_liked };
    })
    .catch((error) => {
      console.error("Error toggling like: ", error);
    });
};

const redirectToRecommendMovies = () => {
  router.go()
};

onMounted(() => {
  fetchRecommendedMovies();
});

onMounted(() => {
  store.getMovies();
});

</script>

<style scoped>
.like{
  margin-left: 140px;
  margin-top: 8px;
}

.scroll-to-top {
  position: fixed;
  bottom: 510px;
  left: 8%; 
  transform: translateX(-50%); 
  z-index: 1000;
  padding: 10px 20px;
  background-color: #51575e;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  text-decoration: none;
}

.scroll-to-top:hover {
  background-color: #0056b3;
}

.title{
  text-align: center;
}
</style>




