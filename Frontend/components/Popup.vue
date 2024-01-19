import Overlay from "ol/Overlay";
import Feature from "ol/Feature";
import { Vector as VectorSource } from 'ol/source';
import { VectorImage } from 'ol/layer';



<template>
    <div id="popup" class="ol-popup">
        <a href="#" id="popup-closer" class="ol-popup-closer"></a>
        <div id="popup-content">
            
                <q-table
                :title="title"
                :rows="rows"
                :columns="columns"
                row-key="key"
                :separator="separator"
                v-model:pagination="table_pagination"
                />
                <q-pagination
                v-model="current"
                color="purple"
                :max="maxPage"
                :max-pages="10"
                boundary-numbers                
                @update:modelValue="onPageChange"
                ></q-pagination>            
        </div>
    </div>
</template>