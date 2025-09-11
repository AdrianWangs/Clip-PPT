<template>
  <div class="slidev-layout two-row-split">
    <!-- First row (full width) -->
    <div class="row-top">
      <slot name="top" />
    </div>
    
    <!-- Second row split into 80/20 -->
    <div class="row-bottom">
      <!-- Left column (80%) -->
      <div class="column-left">
        <slot name="left" />
      </div>
      
      <!-- Right column (20%) -->
      <div class="column-right">
        <slot name="right" />
      </div>
    </div>
  </div>
</template>

<style>
.slidev-layout.two-row-split {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.row-top {
  width: 100%;
  margin-bottom: 2rem;
}

.row-bottom {
  display: flex;
  width: 100%;
  flex: 1;
}

.column-left {
  width: 70%;
  padding-right: 1rem;
}

.column-right {
  width: 30%;
}
</style> 