<template>
  <div class="mx-5">
    <br />
    <div class="row row-cols-2 row-cols-md-4 g-3">
      <template v-for="(review) in displayedReviews" :key="review.id" class="col">
        <template v-if="review.movie == movieId">
          <RouterLink
            :to="{ name: 'ReviewDetail', params: { reviewId: review.id } }"
            class="review-link"
          >
            <div class="card mb-3">
              <div class="card-body">
                <p class="card-text" style="font-weight: bold">
                  {{ review.user }}
                  <span class="rating">
                  <template v-for="n in 5">
                    <i
                      class="fa-solid fa-star"
                      :style="{ color: n <= review.score ? '#FFD43B' : 'grey' }"
                    ></i>
                  </template>
                </span>
                </p>
                <p class="card-text">한줄평: {{ review.title }}</p>
              </div>
            </div>
          </RouterLink>
        </template>
      </template>
    </div>
    <div v-if="store.reviews.length > 4" class="text-center my-3">
      <button @click="toggleShowAll" class="btn btn-primary add">
        {{ showAll ? '접기' : '더보기' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import { useRoute, RouterLink } from "vue-router";
import { useMovieStore } from "@/stores/counter";

const route = useRoute();
//내가 생성한 게시글이 몇번 영화에 쓰였는지 저장 가능
const movieId = ref(route.params.movieId);
const store = useMovieStore();
const showAll = ref(false);

const displayedReviews = computed(() => {
  if (showAll.value) {
    return store.reviews.filter(review => review.movie == movieId.value);
  } else {
    return store.reviews.filter(review => review.movie == movieId.value).slice(0, 4);
  }
});

const toggleShowAll = () => {
  showAll.value = !showAll.value;
};
</script>

<style scoped>
.add {
  position: relative; /* 필수: z-index를 적용하려면 position 속성을 설정해야 합니다 */
  z-index: 10; /*z-index 값은 필요에 따라 조정 가능 */
  color: inherit; /* RouterLink의 기본 색상 유지 */
  text-decoration: none; /* 기본 밑줄 제거 */
}

.review-link {
  text-decoration: none; /* Remove underline from the link */
  color: inherit; /* Inherit the color of the parent element */
}
.rating {
  color: #ffd43b;
}
</style>
