<template>
  <div class="user-info" style="text-align: center">
    <h1>{{ store.name }}</h1>
    <div style="display: inline-block">
      <p style="color: gray">
        팔로워:
        <span style="color: darkgray; font-weight: bold">{{
          followersCount
        }}</span>
        / 팔로잉:
        <span style="color: darkgray; font-weight: bold">{{
          followingCount
        }}</span>
      </p>
    </div>
  </div>

  <hr />
  <!-- 내가 쓴 게시글의 개수 -->
  <div class="centered-content">
    <div class="content-card">
      <p>
        <i class="fa fa-pencil"></i>
        <span style="margin-left: 5px">코멘트 </span><br />
        <span style="font-weight: bold">{{ userReviewCount }}</span>
      </p>

      <!-- 좋아요를 누른 영화의 개수 -->
      <p>
        <i class="fa fa-heart"></i>
        <span style="margin-left: 5px">컬렉션 </span> <br />
        <span style="font-weight: bold">{{ likedMoviesCount }}</span>
      </p>
    </div>
  </div>
  <hr />

  <div style="text-align: center">
    <h4>{{ store.name }}님이 좋아요한 영화</h4>
    <br />

    <template v-for="movie in likedMovies" :key="movie.id">
      <RouterLink :to="{ name: 'moive-detail', params: { movieId: movie.id } }">
        <img
          :src="`https://image.tmdb.org/t/p/w200/${movie.poster_path}`"
          alt="Movie Poster"
        />
      </RouterLink>
    </template>
  </div>
</template>

<script setup>
import { useMovieStore } from "@/stores/counter";
import { useRoute, RouterLink } from "vue-router";
import { ref, onMounted } from "vue";
import axios from "axios";

const store = useMovieStore();
const route = useRoute();

const username = ref(route.params.username);
const isFollowing = ref(false); // 팔로우 상태를 저장할 변수
const followersCount = ref(0); // 팔로워 수를 저장할 변수
const followingCount = ref(0); // 팔로잉 수를 저장할 변수
const likedMoviesCount = ref(0); // 좋아요를 누른 영화의 개수를 저장할 변수
const userReviewCount = ref(0); // 사용자가 쓴 리뷰 개수
const likedMovies = ref([]); // 좋아요를 누른 영화 목록

// 좋아요를 누른 영화 목록을 가져오는 함수
const fetchLikedMovies = () => {
  axios({
    method: "get",
    url: `${store.API_URL}/accounts/liked_movies/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then((response) => {
      likedMovies.value = response.data.movies; // 좋아요를 누른 영화 목록을 업데이트
    })
    .catch((error) => {
      console.error("Error fetching liked movies: ", error);
    });
};

// 초기 상태를 불러오기 위한 함수
const fetchFollowStatus = () => {
  axios({
    method: "get",
    url: `${store.API_URL}/accounts/follow/${store.name}/status/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then((response) => {
      isFollowing.value = response.data.is_following; // 초기 팔로우 상태를 업데이트
      followersCount.value = response.data.followers_count; // 초기 팔로워 수를 업데이트
      followingCount.value = response.data.following_count; // 초기 팔로잉 수를 업데이트
    })
    .catch((error) => {
      console.error("Error fetching follow status: ", error);
    });
};

// 사용자가 작성한 리뷰 개수를 계산하는 함수
const calculateUserReviewCount = () => {
  userReviewCount.value = store.reviews.filter(
    (review) => review.user === store.name
  ).length;
};

// 좋아요를 누른 영화의 개수를 가져오는 함수
const fetchLikedMoviesCount = () => {
  axios({
    method: "get",
    url: `${store.API_URL}/accounts/movie_like_count/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then((response) => {
      likedMoviesCount.value = response.data.liked_movies_count; // 좋아요를 누른 영화의 개수를 업데이트
    })
    .catch((error) => {
      if (error.response && error.response.status === 401) {
        console.error("User not authenticated");
      } else {
        console.error("Error fetching liked movies count: ", error);
      }
    });
};

// 팔로우 상태를 토글하는 함수
const toggleFollow = () => {
  console.log("Button clicked"); // 디버깅 로그
  axios({
    method: "post",
    url: `${store.API_URL}/accounts/follow/${username.value}/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then((response) => {
      isFollowing.value = response.data.is_following; // 팔로우 상태를 업데이트
      // 팔로잉/팔로워 수 업데이트
      if (response.data.is_following) {
        followersCount.value += 1;
      } else {
        followersCount.value -= 1;
      }
      console.log("Follow status updated:", response.data.is_following); // 디버깅 로그
    })
    .catch((error) => {
      console.error("Error toggling follow: ", error);
    });
};

// 컴포넌트가 마운트될 때 초기 팔로우 상태와 좋아요 개수를 가져오고 리뷰 개수를 계산합니다.
onMounted(() => {
  fetchFollowStatus();
  calculateUserReviewCount();
  fetchLikedMoviesCount();
  fetchLikedMovies();
});
</script>

<style scoped>
.user-info {
  margin-top: 30px;
}

.content-card {
  display: flex;
  justify-content: space-around;
  align-items: center;
  text-align: center;
  width: 350px;
  /* box-sizing: border-box; */
  /* background-color: hsl(10, 8%, 15%);
    color: rgb(141, 136, 136); */
  margin-top: 10px;
}

.centered-content {
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
