<template>
  <div class="busca-operadoras">
    <h1>Busca de Operadoras</h1>
    <div class="search-box">
      <input
        type="text"
        v-model="query"
        placeholder="Digite o termo de busca..."
        @keyup.enter="buscar"
      />
      <button @click="buscar">Buscar</button>
    </div>
    <div class="status" v-if="loading">Carregando...</div>
    <div class="status error" v-if="!loading && error">{{ error }}</div>
    <ul v-if="!loading && operadoras.length">
      <li v-for="op in operadoras" :key="op.registro_ans" class="operadora-card">
        <h2>{{ normalizeText(op.razao_social) }}</h2>
        <p><strong>CNPJ:</strong> {{ normalizeText(op.cnpj) }}</p>
        <p><strong>Modalidade:</strong> {{ normalizeText(op.modalidade) }}</p>
      </li>
    </ul>
    <div v-else-if="!loading && query" class="status">
      Nenhuma operadora encontrada.
    </div>
  </div>
</template>

<script>
let mojibake;
try {
  mojibake = require("mojibake");
} catch (e) {
  console.error("Erro ao importar mojibake:", e);
  mojibake = (str) => str; 
}

export default {
  name: "BuscaOperadoras",
  data() {
    return {
      query: "",
      operadoras: [],
      loading: false,
      error: ""
    };
  },
  methods: {
    async buscar() {
      this.loading = true;
      this.error = "";
      try {
        const response = await fetch(`http://localhost:8000/operadoras?q=${encodeURIComponent(this.query)}`);
        if (!response.ok) {
          this.error = "Operadora não encontrada";
          this.operadoras = [];
          throw new Error("Operadora não encontrada");
        }
        const data = await response.json();
        console.log("Dados recebidos:", data);
        this.operadoras = data;
      } catch (err) {
        console.error(err);
        this.operadoras = [];
      } finally {
        this.loading = false;
      }
    },
    normalizeText(str) {
      if (!str) return "";
      return mojibake(str).trim();
    }
  }
};
</script>

<style scoped>
.busca-operadoras {
  max-width: 800px;
  margin: 30px auto;
  padding: 20px;
  font-family: 'Helvetica Neue', Arial, sans-serif;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
h1 {
  text-align: center;
  margin-bottom: 20px;
  color: #333;
}
.search-box {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}
.search-box input {
  padding: 10px;
  font-size: 16px;
  width: 300px;
  border: 1px solid #ccc;
  border-radius: 4px;
}
.search-box button {
  padding: 10px 20px;
  font-size: 16px;
  margin-left: 10px;
  border: none;
  background-color: #3498db;
  color: #fff;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}
.search-box button:hover {
  background-color: #2980b9;
}
.status {
  text-align: center;
  font-size: 18px;
  color: #666;
  margin-top: 20px;
}
.status.error {
  color: red;
}
ul {
  list-style: none;
  padding: 0;
}
.operadora-card {
  background-color: #f9f9f9;
  border: 1px solid #eee;
  border-radius: 4px;
  padding: 15px;
  margin-bottom: 15px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}
.operadora-card h2 {
  margin: 0 0 10px;
  font-size: 20px;
  color: #333;
}
.operadora-card p {
  margin: 5px 0;
  font-size: 16px;
  color: #555;
}
</style>
