<template>
  <div>
  <h2>サービスの概要</h2>
    <p>このアンケートは「講義終了後の感想アンケートから, その人の定期テスト点を予測するwebアプリ」
      の社会的価値が適切か否かを客観的に把握することを目的としています。</p>
    <button @click="$emit('next')">次へ</button>
  </div>
</template>
