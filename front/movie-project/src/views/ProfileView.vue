<template>
  <template v-if="username === store.name">
    <MyProfile />
  </template>

  <template v-else>
    <div class="user-info" style="text-align: center">
      <h1>{{ username }}</h1>
      <div style="display: inline-block">
        <button
          type="button"
          class="btn btn-outline-secondary btn-sm"
          @click.prevent="toggleFollow"
          v-if="store.isLogin"
        >
          {{ isFollowing ? "언팔로우" : "팔로우" }}
        </button>
        <br>
        <div style="display: inline-block; margin-top: 5px;">
          <p style="color: gray">
            팔로워:
            <span style="color: darkgray; font-weight: bold">{{ followersCount }}</span>
            / 팔로잉:
            <span style="color: darkgray; font-weight: bold">{{ followingCount }}</span>
          </p>
        </div>
      </div>
    </div>

    <hr />
    <div class="centered-content">
      <div class="content-card">
        <p>
          <i class="fa fa-pencil"></i>
          <span style="margin-left: 5px">코멘트 </span><br />
          <span style="font-weight: bold">{{ userReviewCount }}</span>
        </p>
        <p>
          <i class="fa fa-heart"></i>
          <span style="margin-left: 5px">컬렉션 </span> <br />
          <span style="font-weight: bold">{{ likedMoviesCount }}</span>
        </p>
      </div>
    </div>
    <hr />

    <div style="text-align: center">
      <h4>{{ username }}님이 좋아요한 영화</h4>
      <br />
      <template v-for="movie in likedMovies" :key="movie.id">
        <!-- <RouterLink :to="{ name: 'movie-detail', params: { movieId: movie.id } }"> -->
          <img :src="`https://image.tmdb.org/t/p/w200/${movie.poster_path}`" alt="Movie Poster" />
        <!-- </RouterLink> -->
      </template>
    </div>
  </template>
</template>

<script setup>
import { useMovieStore } from "@/stores/counter";
import { useRoute } from "vue-router";
import { ref, onMounted } from "vue";
import axios from "axios";
import MyProfile from "@/components/MyProfile.vue";

const store = useMovieStore();
const route = useRoute();

const username = ref(route.params.username);
const isFollowing = ref(false);
const followersCount = ref(0);
const followingCount = ref(0);
const userReviewCount = ref(0);
const likedMoviesCount = ref(0);
const likedMovies = ref([]);


// 유저가 좋아요한 영화를 가져오는 함수
const fetchLikedMovies = () => {
  axios({
    method: "get",
    url: `${store.API_URL}/accounts/profile/${username.value}/liked-movies/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
  .then((response) => {
    likedMovies.value = response.data;
  })
  .catch((error) => {
    console.error("Error fetching liked movies: ", error);
  });
};


// 사용자 프로필 데이터를 가져오는 함수
const fetchUserProfileData = () => {
  axios({
    method: "get",
    url: `${store.API_URL}/accounts/follow/${username.value}/status/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
  .then((response) => {
    const data = response.data;
    followersCount.value = data.followers_count;
    followingCount.value = data.following_count;
    isFollowing.value = data.is_following; // 팔로우 상태를 서버에서 가져옴
  })
  .catch((error) => {
    console.error("Error fetching user profile data: ", error);
  });
};

const fetchFollowStatus = () => {
  axios({
    method: "get",
    url: `${store.API_URL}/accounts/follow/${username.value}/status/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
  .then((response) => {
    isFollowing.value = response.data.is_following;
    followersCount.value = response.data.followers_count;
    followingCount.value = response.data.following_count;
  })
  .catch((error) => {
    console.error("Error fetching follow status: ", error);
  });
};


// 팔로우 버튼 토글 함수
const toggleFollow = () => {
  axios({
    method: "post",
    url: `${store.API_URL}/accounts/follow/${username.value}/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
  .then((response) => {
    isFollowing.value = response.data.is_following;
    if (isFollowing.value) {
      followersCount.value += 1;
    } else if (followersCount.value > 0) {
      followersCount.value -= 1;
    }
  })
  .catch((error) => {
    console.error("Error toggling follow: ", error);
  });
};

// 사용자가 작성한 리뷰 개수를 계산하는 함수
const calculateUserReviewCount = () => {
  userReviewCount.value = store.reviews.filter(
    (review) => review.user === username.value
  ).length;
};


onMounted(() => {
  fetchUserProfileData();
  calculateUserReviewCount();
  fetchFollowStatus();
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
  margin-top: 10px;
}

.centered-content {
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
