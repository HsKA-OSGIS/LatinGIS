<template>

<div class=" bg-white max-w-md mx-auto bg-white rounded-xl overflow-hidden p-6 shadow-md">
    <h2 class="text-2xl font-semibold mb-4">Map Controls</h2>
      <div class="flex flex-wrap space-x-2">
            <!-- Map Layer Options (Example options, replace with your actual options) -->
        <!-- Map Layers Section -->
    <div class="mb-4">
        <h3 class="text-lg font-semibold mb-2">Map Layers</h3>
          <label class="flex items-center space-x-1">
                <input type="checkbox" class="form-checkbox text-indigo-500"  @click="toggleLayer('Hotels')" >
                <span>Layer 1</span>
            </label>
            <label class="flex items-center space-x-1">
                <input type="checkbox" class="form-checkbox">
                <span>Layer 2</span>
            </label>
            <label class="flex items-center space-x-1">
                <input type="checkbox" class="form-checkbox">
                <span>Layer 3</span>
            </label>
            <label class="flex items-center space-x-1">
                <input type="checkbox" class="form-checkbox" >
                <span>My location</span>
            </label>
        </div>
    </div>

    <!-- WPS Parameters Section -->
    <div class="mb-4">
        <h3 class="text-lg font-semibold mb-2">WPS Parameters</h3>
        <div class="flex flex-wrap space-x-2">
            <!-- WPS Parameter Options (Example options, replace with your actual options) -->
            <label class="flex items-center space-x-1">
                <input type="checkbox" class="form-checkbox">
                <span>Walking</span>
            </label>
            <label class="flex items-center space-x-1">
                <input type="checkbox" class="form-checkbox">
                <span>Bike</span>
            </label>
            <!-- Add more parameters as needed -->
        </div>
    </div>

    <!-- Travel Distance Section -->
    <div>
        <h3 class="text-lg font-semibold mb-2">Travel Distance</h3>
        <div class="flex items-center space-x-2">
            <!-- Travel Distance Options (Example options, replace with your actual options) -->
            <label class="flex items-center space-x-1">
                <input type="radio" class="form-radio" name="distance" value="short">
                <span>15 min</span>
            </label>
            <label class="flex items-center space-x-1">
                <input type="radio" class="form-radio" name="distance" value="medium">
                <span>30 min</span>
            </label>
            <label class="flex items-center space-x-1">
                <input type="radio" class="form-radio" name="distance" value="long">
                <span>45 min</span>
            </label>
        </div>
    </div>
     <!-- Calculate Button (Centered) -->
     <div class="flex justify-center mt-4">
     <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
  Calculate
</button>
</div>
</div>
</template>

<script setup>


const toggleLayer = (layerName) => {
  // Emit a custom event with the layerName
  emit('toggleLayer', layerName);
};
</script>