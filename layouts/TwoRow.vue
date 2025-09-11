<template>
  <div class="slidev-layout two-row-split">
    
    <!-- Second row split into 80/20 -->
    <div class="row-bottom">
      <div class="column-left-1">
        <slot name="left" />
      </div>
      
      <!-- Right column (20%) -->
      <div class="column-right-1">
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


.row-bottom {
  display: flex;
  width: 100%;
  flex: 1;
}

.column-left-1 {
  width: 60%;
  padding-right: 1rem;
}

.column-right-1 {
  width: 40%;
}
</style> 