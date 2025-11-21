import { defineComponent } from 'vue'
import { Card, Avatar, Button } from 'ant-design-vue'
import { CodeOutlined, SearchOutlined, BarChartOutlined, GlobalOutlined } from '@ant-design/icons-vue'

export const CapabilityShowcase = defineComponent({
  name: 'CapabilityShowcase',
  props: {
    data: {
      type: Object,
      required: true
    }
  },
  setup(props) {
    const handleCapabilityClick = (capability: any) => {
      // Emit event or handle capability selection
      console.log('Selected capability:', capability)
    }

    const getIcon = (iconName: string) => {
      const icons: Record<string, any> = {
        'CodeOutlined': CodeOutlined,
        'SearchOutlined': SearchOutlined,
        'BarChartOutlined': BarChartOutlined,
        'GlobalOutlined': GlobalOutlined
      }
      return icons[iconName] || CodeOutlined
    }

    return {
      handleCapabilityClick,
      getIcon
    }
  },
  template: `
    <div class="capability-showcase">
      <h3>{{ data.title }}</h3>
      <div class="capabilities-grid">
        <div 
          v-for="capability in data.capabilities"
          :key="capability.name"
          class="capability-card"
          @click="handleCapabilityClick(capability)"
        >
          <a-card hoverable>
            <div class="capability-content">
              <div class="capability-icon">
                <component :is="getIcon(capability.icon)" />
              </div>
              <div class="capability-info">
                <h4>{{ capability.name }}</h4>
                <p>{{ capability.description }}</p>
              </div>
            </div>
          </a-card>
        </div>
      </div>
    </div>
  `
})

export default CapabilityShowcase