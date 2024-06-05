<template>
  <div v-for="movie in store.movies" :key="movie.id" class="movie-container">
    <template v-if="movie.id == movieId">
      <div class="poster-container">
        <img
          :src="`https://image.tmdb.org/t/p/w200/${movie.poster_path}`"
          alt="Movie Poster"
          class="movie-poster-background"
        />
        <img
          :src="`https://image.tmdb.org/t/p/w200/${movie.poster_path}`"
          alt="Movie Poster"
          class="movie-poster-overlay"
        />
      </div>
    
      <div class="explain">
        <p>
          감독: &nbsp;
          <span v-for="director in movie.directors" :key="director.id">
            {{ director.name }} &nbsp;
          </span>
        </p>
        <p>
          배우:&nbsp;
          <span
            v-for="(actor, index) in movie.actors.slice(
              0,
              showAllActors ? undefined : 5
            )"
            :key="actor.id"
          >
            {{ actor.name }} &nbsp;
            <template v-if="index === 4 && !showAllActors">
              <button
                @click="showAllActors = true"
                class="btn btn-link text-white-50"
              >
                더 보기
              </button>
            </template>
          </span>
          <span v-if="showAllActors">
            <button
              @click="showAllActors = false"
              class="btn btn-link text-white-50"
            >
              간략히 보기
            </button>
          </span>
        </p>
        <p>
          장르:&nbsp;
          <span v-for="genre in movie.genres" :key="genre.id">
            {{ genre.name }} &nbsp;
          </span>
        </p>
        <p>개봉일: {{ movie.release_date }}</p>
        <p>줄거리: {{ movie.overview }}</p>
        <p style="vertical-align: middle;"><i class="fa-solid fa-star" style="color: yellow"></i>  {{ movie.vote_average.toFixed(1) }}</p>
        <p class="icon">
        <button @click="toggleLike" class="btn btn-lg" v-if="store.isLogin" style="vertical-align: middle;">
          <i v-if="isLiked" class="fa-solid fa-heart" style="color: #ff0000; font-size: 30px; vertical-align: middle;"></i>
          <i v-else class="fa-regular fa-heart" style="color: #ff0000; font-size: 30px; vertical-align: middle;"></i>
          <!-- {{ isLiked ? "좋아요 취소" : "좋아요" }} -->
        </button>
        <!-- 리뷰생성 모달로 구현 -->
        <button @click="showModal = true" class="btn" data-bs-toggle="modal" data-bs-target="#exampleModal" data-bs-whatever="Movie Review" v-if="store.isLogin" style="vertical-align: middle;">
          <i class="fa-regular fa-pen-to-square" style="color: blueviolet; font-size: 30px; vertical-align: middle;"></i>
        </button>
        </p>  

          <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered">
              <div class="modal-content">
                <div class="modal-header" style="border-bottom: none;">
                  <h3 style="color: black;">{{ movie.title }}</h3>
                  <button type="button" class="btn-close" aria-label="Close" @click="closeModal"></button>
                </div>
                <div class="modal-body">
                  <form @submit.prevent="createReview">
                    <div class="mb-3">
                      <!-- <label for="title" class="col-form-label" style="color: black;">한줄평:</label> -->
                      <input type="text" id="title" v-model.trim="title" class="form-control" placeholder="한줄평을 입력하세요.">
                    </div>
                    <div class="mb-3">
                      <!-- <label for="content" class="col-form-label" style="color: black;">리뷰:</label> -->
                      <textarea id="content" v-model.trim="content" class="form-control" rows="6" placeholder="리뷰를 입력하세요."></textarea>
                    </div>
                    <div class="mb-3">
                      <i class="fa-regular fa-star" @click="changeScore(1)" :style="{ color: score >= 1 ? '#FFD43B' : 'grey', fontSize: '32px', 'fill': score >= 1 ? '#FFD43B' : 'transparent' }"></i>
                      <i class="fa-regular fa-star" @click="changeScore(2)" :style="{ color: score >= 2 ? '#FFD43B' : 'grey', fontSize: '32px', 'fill': score >= 2 ? '#FFD43B' : 'transparent' }"></i>
                      <i class="fa-regular fa-star" @click="changeScore(3)" :style="{ color: score >= 3 ? '#FFD43B' : 'grey', fontSize: '32px', 'fill': score >= 3 ? '#FFD43B' : 'transparent' }"></i>
                      <i class="fa-regular fa-star" @click="changeScore(4)" :style="{ color: score >= 4 ? '#FFD43B' : 'grey', fontSize: '32px', 'fill': score >= 4 ? '#FFD43B' : 'transparent' }"></i>
                      <i class="fa-regular fa-star" @click="changeScore(5)" :style="{ color: score >= 5 ? '#FFD43B' : 'grey', fontSize: '32px', 'fill': score >= 5 ? '#FFD43B' : 'transparent' }"></i>
                    </div>
                    <div class="mb-3 text-center"> <!-- 가운데 정렬을 위한 text-center 클래스 추가 -->
                      <input type="submit" value="작성하기" class="btn btn-secondary">
                    </div>
                  </form>
                </div>
              </div>
            </div>
          </div>
        </div>
      
    </template>
    </div>
    <ReviewList />
</template>




<script setup>
import { useMovieStore } from "@/stores/counter";
import { onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import ReviewList from "@/components/ReviewList.vue";
import axios from "axios";
// import { watch } from 'vue';

const store = useMovieStore();

onMounted(() => {
  store.getMovies();
});

onMounted(() => {
  store.getReviews();
});

const route = useRoute();
const movieId = ref(route.params.movieId);
const showAllActors = ref(false);
const score = ref(0);

const isLiked = ref(false); // 좋아요 상태를 저장할 변수

// 좋아요 상태를 불러오기 위한 함수
const fetchLikeStatus = () => {
  axios({
    method: "get",
    url: `${store.API_URL}/accounts/movies/${movieId.value}/like-status/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then((response) => {
      isLiked.value = response.data.is_liked; // 초기 좋아요 상태를 업데이트
    })
    .catch((error) => {
      console.error("Error fetching like status: ", error);
    });
};

// 좋아요 상태를 토글하는 함수
const toggleLike = () => {
  axios({
    method: "post",
    url: `${store.API_URL}/accounts/movies/${movieId.value}/toggle-like/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then((response) => {
      isLiked.value = response.data.is_liked; // 좋아요 상태를 업데이트
    })
    .catch((error) => {
      console.error("Error toggling like: ", error);
    });
};



// 컴포넌트가 마운트될 때 초기 좋아요 상태를 가져옵니다.
onMounted(() => {
  fetchLikeStatus();
});

const showModal = ref(false);

const title = ref(''); // 한줄평 초기화
const content = ref(''); // 리뷰 초기화


const closeModal = () => {
  showModal.value = false;
  const myModalEl = document.getElementById('exampleModal');
  const modal = bootstrap.Modal.getInstance(myModalEl)
  resetFormFields()
  modal.hide();
};

const createReview = () => {
  if (!title.value || !content.value) {
    alert('제목과 내용을 모두 입력해주세요.');
    return;
  }

  axios({
    method: 'post',
    url: `${store.API_URL}/reviews/`,
    data: {
      title: title.value,
      content: content.value,
      movie: movieId.value,
      score: score.value,
    },
    headers: {
      Authorization: `Token ${store.token}`,
      'Content-Type': 'application/json'
    },
  })
  .then(() => {
    closeModal(); // 모달 닫기
    store.getReviews(); 
    resetFormFields()  // 폼 필드 초기화
  })
  .catch((err) => console.log(err));
};

const changeScore = (newScore) => {
  score.value = newScore;
};

const resetFormFields = () => {
  title.value = '';
  content.value = '';
  score.value = 0;
};

</script>

<style scoped>
.movie-container {
  position: relative;
}

.poster-container {
  position: relative;
}

.movie-poster-background {
  width: 100%;
  height: 600px;
  opacity: 0.19;
  transform: scale(2); /*포스터 확대*/
  /*height: 66vh;  화면 세로 길이의 3분의 2 */
  object-fit: cover; /* 이미지가 잘리지 않도록 */
}

.movie-poster-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 300px;
  height: auto;
  opacity: 1; /* 투명도를 설정하지 않음 */
  margin-left: 70px;
  margin-top: 40px;
}

.explain {
  position: absolute;
  top: 0;
  left: 430px;
  margin-top: 70px;
  margin-right: 75px;
}

/* .review-btn {
  margin-top: 20px;
  padding: 0;
} */

.icon {
  margin-left: -20px;
}
</style>
