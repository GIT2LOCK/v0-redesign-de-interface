"use client"

import { useState, useRef, useEffect } from "react"
import { motion, AnimatePresence } from "framer-motion"
import {
  FileSpreadsheet,
  Terminal,
  User,
  History,
  Upload,
  Play,
  Trash2,
  Download,
  CheckCircle2,
  Clock,
  AlertCircle,
  X,
  Settings,
  Moon,
  Sun,
  ChevronRight,
  Search,
  Filter,
  RefreshCw,
} from "lucide-react"
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import { Badge } from "@/components/ui/badge"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip"

type TabType = "dashboard" | "planilha" | "log" | "historico" | "usuario"

interface LogEntry {
  id: number
  timestamp: string
  message: string
  type: "info" | "success" | "warning" | "error"
}

interface ProcessingRecord {
  id: number
  date: string
  fileName: string
  status: "success" | "error" | "processing"
  records: number
  duration: string
}

interface SpreadsheetRow {
  id: number
  cnpj: string
  razaoSocial: string
  valor: string
  status: "pendente" | "processado" | "erro"
}

const tabs = [
  { id: "dashboard" as TabType, label: "Dashboard", icon: FileSpreadsheet },
  { id: "planilha" as TabType, label: "Planilha", icon: FileSpreadsheet },
  { id: "log" as TabType, label: "Log", icon: Terminal },
  { id: "historico" as TabType, label: "Histórico", icon: History },
  { id: "usuario" as TabType, label: "Usuário", icon: User },
]

export function NFSeAutomation() {
  const [activeTab, setActiveTab] = useState<TabType>("dashboard")
  const [isDarkMode, setIsDarkMode] = useState(true)
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [isProcessing, setIsProcessing] = useState(false)
  const [searchTerm, setSearchTerm] = useState("")
  const fileInputRef = useRef<HTMLInputElement>(null)

  // Sincroniza o tema com a classe do documento
  useEffect(() => {
    if (isDarkMode) {
      document.documentElement.classList.add("dark")
    } else {
      document.documentElement.classList.remove("dark")
    }
  }, [isDarkMode])

  const [logs, setLogs] = useState<LogEntry[]>([
    { id: 1, timestamp: "11:58:01", message: "Interface iniciada com sucesso. Aguardando arquivo...", type: "info" },
    { id: 2, timestamp: "11:58:05", message: "Sistema pronto para processamento", type: "success" },
  ])

  const [processingHistory, setProcessingHistory] = useState<ProcessingRecord[]>([
    { id: 1, date: "28/05/2026 10:30", fileName: "notas_maio.xlsx", status: "success", records: 150, duration: "2m 34s" },
    { id: 2, date: "27/05/2026 15:45", fileName: "notas_abril.xlsx", status: "success", records: 98, duration: "1m 45s" },
    { id: 3, date: "26/05/2026 09:15", fileName: "notas_extra.xlsx", status: "error", records: 45, duration: "0m 30s" },
  ])

  const [spreadsheetData, setSpreadsheetData] = useState<SpreadsheetRow[]>([
    { id: 1, cnpj: "12.345.678/0001-90", razaoSocial: "Empresa ABC Ltda", valor: "R$ 1.500,00", status: "pendente" },
    { id: 2, cnpj: "98.765.432/0001-10", razaoSocial: "Comércio XYZ ME", valor: "R$ 2.300,00", status: "processado" },
    { id: 3, cnpj: "11.222.333/0001-44", razaoSocial: "Serviços Tech SA", valor: "R$ 890,00", status: "erro" },
    { id: 4, cnpj: "55.666.777/0001-88", razaoSocial: "Consultoria Beta", valor: "R$ 4.200,00", status: "pendente" },
  ])

  const user = {
    name: "Carlos Silva",
    email: "carlos.silva@2lock.com.br",
    role: "Administrador",
    avatar: "/placeholder-user.jpg",
    lastLogin: "28/05/2026 às 09:15",
    totalProcessed: 1245,
    successRate: 98.5,
  }

  const addLog = (message: string, type: LogEntry["type"]) => {
    const now = new Date()
    const timestamp = now.toLocaleTimeString("pt-BR", { hour: "2-digit", minute: "2-digit", second: "2-digit" })
    setLogs(prev => [...prev, { id: Date.now(), timestamp, message, type }])
  }

  const handleFileSelect = () => {
    fileInputRef.current?.click()
  }

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      setSelectedFile(file)
      addLog(`Arquivo selecionado: ${file.name}`, "info")
    }
  }

  const handleProcess = () => {
    if (!selectedFile) {
      addLog("Nenhum arquivo selecionado!", "warning")
      return
    }

    setIsProcessing(true)
    addLog("Iniciando processamento...", "info")

    // Simulate processing
    setTimeout(() => {
      addLog("Validando dados da planilha...", "info")
    }, 500)

    setTimeout(() => {
      addLog("Processando notas fiscais...", "info")
    }, 1500)

    setTimeout(() => {
      setIsProcessing(false)
      addLog("Processamento concluído com sucesso!", "success")
      
      const newRecord: ProcessingRecord = {
        id: Date.now(),
        date: new Date().toLocaleString("pt-BR"),
        fileName: selectedFile.name,
        status: "success",
        records: Math.floor(Math.random() * 100) + 50,
        duration: `${Math.floor(Math.random() * 3)}m ${Math.floor(Math.random() * 60)}s`,
      }
      setProcessingHistory(prev => [newRecord, ...prev])
    }, 3000)
  }

  const clearLogs = () => {
    setLogs([])
    addLog("Log limpo", "info")
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case "success":
      case "processado":
        return "bg-emerald-500/20 text-emerald-400 border-emerald-500/30"
      case "error":
      case "erro":
        return "bg-red-500/20 text-red-400 border-red-500/30"
      case "processing":
        return "bg-amber-500/20 text-amber-400 border-amber-500/30"
      default:
        return "bg-blue-500/20 text-blue-400 border-blue-500/30"
    }
  }

  const getLogIcon = (type: LogEntry["type"]) => {
    switch (type) {
      case "success":
        return <CheckCircle2 className="w-4 h-4 text-emerald-400" />
      case "warning":
        return <AlertCircle className="w-4 h-4 text-amber-400" />
      case "error":
        return <X className="w-4 h-4 text-red-400" />
      default:
        return <Clock className="w-4 h-4 text-blue-400" />
    }
  }

  return (
    <TooltipProvider>
      <div className="min-h-screen gradient-bg">
        {/* Animated background orbs */}
        <div className="fixed inset-0 overflow-hidden pointer-events-none">
          <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-primary/10 rounded-full blur-3xl animate-pulse-glow" />
          <div className="absolute bottom-1/4 right-1/4 w-80 h-80 bg-accent/10 rounded-full blur-3xl animate-pulse-glow" style={{ animationDelay: "1.5s" }} />
        </div>

        <div className="relative z-10 flex flex-col h-screen">
          {/* Header */}
          <motion.header
            initial={{ y: -20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            className="glass border-b border-border/50 px-6 py-4"
          >
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-4">
                {/* Logo */}
                <div className="flex items-center gap-3">
                  <div className="relative">
                    <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-primary to-accent flex items-center justify-center glow-primary">
                      <span className="text-lg font-bold text-primary-foreground">2L</span>
                    </div>
                    <div className="absolute -bottom-1 -right-1 w-3 h-3 bg-emerald-500 rounded-full border-2 border-background" />
                  </div>
                  <div>
                    <h1 className="text-xl font-bold bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
                      2LOCK
                    </h1>
                    <p className="text-xs text-muted-foreground">Automação NFS-e</p>
                  </div>
                </div>
              </div>

              <div className="flex items-center gap-3">
                <Tooltip>
                  <TooltipTrigger asChild>
                    <Button
                      variant="ghost"
                      size="icon"
                      className="glass-card hover:glow-primary transition-all duration-300"
                      onClick={() => setIsDarkMode(!isDarkMode)}
                    >
                      {isDarkMode ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
                    </Button>
                  </TooltipTrigger>
                  <TooltipContent>Alternar tema</TooltipContent>
                </Tooltip>

                <Tooltip>
                  <TooltipTrigger asChild>
                    <Button variant="ghost" size="icon" className="glass-card hover:glow-primary transition-all duration-300">
                      <Settings className="w-5 h-5" />
                    </Button>
                  </TooltipTrigger>
                  <TooltipContent>Configurações</TooltipContent>
                </Tooltip>

                <Button variant="ghost" size="icon" className="glass-card hover:bg-red-500/20 transition-all duration-300">
                  <X className="w-5 h-5" />
                </Button>
              </div>
            </div>
          </motion.header>

          <div className="flex flex-1 overflow-hidden">
            {/* Sidebar Navigation */}
            <motion.nav
              initial={{ x: -20, opacity: 0 }}
              animate={{ x: 0, opacity: 1 }}
              transition={{ delay: 0.1 }}
              className="w-64 glass border-r border-border/50 p-4 flex flex-col gap-2"
            >
              {tabs.map((tab, index) => (
                <motion.button
                  key={tab.id}
                  initial={{ x: -20, opacity: 0 }}
                  animate={{ x: 0, opacity: 1 }}
                  transition={{ delay: 0.1 + index * 0.05 }}
                  onClick={() => setActiveTab(tab.id)}
                  className={cn(
                    "flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-300 group",
                    activeTab === tab.id
                      ? "glass-card glow-primary text-primary"
                      : "hover:glass-card text-muted-foreground hover:text-foreground"
                  )}
                >
                  <tab.icon className={cn(
                    "w-5 h-5 transition-all duration-300",
                    activeTab === tab.id && "text-primary"
                  )} />
                  <span className="font-medium">{tab.label}</span>
                  <ChevronRight className={cn(
                    "w-4 h-4 ml-auto transition-all duration-300 opacity-0 -translate-x-2",
                    activeTab === tab.id && "opacity-100 translate-x-0"
                  )} />
                </motion.button>
              ))}

              {/* Stats Card */}
              <motion.div
                initial={{ y: 20, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 0.4 }}
                className="mt-auto glass-card rounded-2xl p-4"
              >
                <div className="flex items-center gap-3 mb-4">
                  <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-emerald-500 to-blue-500 flex items-center justify-center">
                    <CheckCircle2 className="w-5 h-5 text-white" />
                  </div>
                  <div>
                    <p className="text-sm text-muted-foreground">Taxa de sucesso</p>
                    <p className="text-xl font-bold text-emerald-400">98.5%</p>
                  </div>
                </div>
                <div className="h-2 bg-muted rounded-full overflow-hidden">
                  <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: "98.5%" }}
                    transition={{ delay: 0.6, duration: 1 }}
                    className="h-full bg-gradient-to-r from-emerald-500 to-blue-500 rounded-full"
                  />
                </div>
              </motion.div>
            </motion.nav>

            {/* Main Content */}
            <main className="flex-1 p-6 overflow-auto">
              <AnimatePresence mode="wait">
                {activeTab === "dashboard" && (
                  <DashboardTab
                    key="dashboard"
                    selectedFile={selectedFile}
                    isProcessing={isProcessing}
                    logs={logs}
                    onFileSelect={handleFileSelect}
                    onProcess={handleProcess}
                    onClearLogs={clearLogs}
                    getLogIcon={getLogIcon}
                    fileInputRef={fileInputRef}
                    onFileChange={handleFileChange}
                  />
                )}
                {activeTab === "planilha" && (
                  <PlanilhaTab
                    key="planilha"
                    data={spreadsheetData}
                    searchTerm={searchTerm}
                    setSearchTerm={setSearchTerm}
                    getStatusColor={getStatusColor}
                  />
                )}
                {activeTab === "log" && (
                  <LogTab
                    key="log"
                    logs={logs}
                    onClearLogs={clearLogs}
                    getLogIcon={getLogIcon}
                  />
                )}
                {activeTab === "historico" && (
                  <HistoricoTab
                    key="historico"
                    history={processingHistory}
                    getStatusColor={getStatusColor}
                  />
                )}
                {activeTab === "usuario" && (
                  <UsuarioTab
                    key="usuario"
                    user={user}
                  />
                )}
              </AnimatePresence>
            </main>
          </div>
        </div>

        <input
          type="file"
          ref={fileInputRef}
          onChange={handleFileChange}
          accept=".xlsx,.xls,.csv"
          className="hidden"
        />
      </div>
    </TooltipProvider>
  )
}

// Dashboard Tab
function DashboardTab({
  selectedFile,
  isProcessing,
  logs,
  onFileSelect,
  onProcess,
  onClearLogs,
  getLogIcon,
  fileInputRef,
  onFileChange,
}: {
  selectedFile: File | null
  isProcessing: boolean
  logs: LogEntry[]
  onFileSelect: () => void
  onProcess: () => void
  onClearLogs: () => void
  getLogIcon: (type: LogEntry["type"]) => React.ReactNode
  fileInputRef: React.RefObject<HTMLInputElement | null>
  onFileChange: (e: React.ChangeEvent<HTMLInputElement>) => void
}) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      className="space-y-6"
    >
      {/* File Upload Area */}
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ delay: 0.1 }}
        className="glass-card rounded-2xl p-6"
      >
        <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
          <Upload className="w-5 h-5 text-primary" />
          Seleção de Arquivo
        </h2>
        
        <div
          onClick={onFileSelect}
          className="border-2 border-dashed border-border/50 rounded-xl p-8 text-center cursor-pointer hover:border-primary/50 hover:bg-primary/5 transition-all duration-300 group"
        >
          <motion.div
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="w-16 h-16 rounded-2xl bg-gradient-to-br from-primary/20 to-accent/20 flex items-center justify-center mx-auto mb-4 group-hover:glow-primary transition-all duration-300"
          >
            <FileSpreadsheet className="w-8 h-8 text-primary" />
          </motion.div>
          {selectedFile ? (
            <div>
              <p className="font-medium text-foreground">{selectedFile.name}</p>
              <p className="text-sm text-muted-foreground mt-1">
                {(selectedFile.size / 1024).toFixed(2)} KB
              </p>
            </div>
          ) : (
            <div>
              <p className="font-medium text-foreground">Clique para selecionar um arquivo</p>
              <p className="text-sm text-muted-foreground mt-1">
                Suporta arquivos .xlsx, .xls e .csv
              </p>
            </div>
          )}
        </div>

        <div className="flex gap-3 mt-4">
          <Button
            onClick={onFileSelect}
            variant="outline"
            className="flex-1 glass-card border-primary/30 hover:bg-primary/10 hover:border-primary/50 transition-all duration-300"
          >
            <Upload className="w-4 h-4 mr-2" />
            Selecionar Planilha
          </Button>
          <Button
            onClick={onProcess}
            disabled={!selectedFile || isProcessing}
            className="flex-1 bg-gradient-to-r from-primary to-accent hover:opacity-90 glow-primary transition-all duration-300"
          >
            {isProcessing ? (
              <>
                <RefreshCw className="w-4 h-4 mr-2 animate-spin" />
                Processando...
              </>
            ) : (
              <>
                <Play className="w-4 h-4 mr-2" />
                Confirmar e Processar
              </>
            )}
          </Button>
        </div>
      </motion.div>

      {/* Quick Log Preview */}
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ delay: 0.2 }}
        className="glass-card rounded-2xl p-6"
      >
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold flex items-center gap-2">
            <Terminal className="w-5 h-5 text-primary" />
            Log de Execução
          </h2>
          <Button
            variant="ghost"
            size="sm"
            onClick={onClearLogs}
            className="text-muted-foreground hover:text-foreground"
          >
            <Trash2 className="w-4 h-4 mr-2" />
            Limpar
          </Button>
        </div>

        <div className="bg-background/50 rounded-xl p-4 h-48 overflow-y-auto font-mono text-sm">
          {logs.slice(-10).map((log, index) => (
            <motion.div
              key={log.id}
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.05 }}
              className="flex items-start gap-3 py-1.5"
            >
              {getLogIcon(log.type)}
              <span className="text-muted-foreground">{log.timestamp}</span>
              <span className={cn(
                log.type === "success" && "text-emerald-400",
                log.type === "warning" && "text-amber-400",
                log.type === "error" && "text-red-400",
                log.type === "info" && "text-foreground"
              )}>
                {log.message}
              </span>
            </motion.div>
          ))}
        </div>
      </motion.div>
    </motion.div>
  )
}

// Planilha Tab
function PlanilhaTab({
  data,
  searchTerm,
  setSearchTerm,
  getStatusColor,
}: {
  data: SpreadsheetRow[]
  searchTerm: string
  setSearchTerm: (term: string) => void
  getStatusColor: (status: string) => string
}) {
  const filteredData = data.filter(row =>
    row.razaoSocial.toLowerCase().includes(searchTerm.toLowerCase()) ||
    row.cnpj.includes(searchTerm)
  )

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      className="space-y-6"
    >
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className="glass-card rounded-2xl p-6"
      >
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-lg font-semibold flex items-center gap-2">
            <FileSpreadsheet className="w-5 h-5 text-primary" />
            Dados da Planilha
          </h2>
          <div className="flex items-center gap-3">
            <div className="relative">
              <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground" />
              <Input
                placeholder="Buscar..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-9 w-64 glass-input"
              />
            </div>
            <Button variant="outline" size="icon" className="glass-card">
              <Filter className="w-4 h-4" />
            </Button>
          </div>
        </div>

        <div className="rounded-xl overflow-hidden border border-border/50">
          <Table>
            <TableHeader>
              <TableRow className="bg-muted/30 hover:bg-muted/30">
                <TableHead className="text-foreground font-semibold">CNPJ</TableHead>
                <TableHead className="text-foreground font-semibold">Razão Social</TableHead>
                <TableHead className="text-foreground font-semibold">Valor</TableHead>
                <TableHead className="text-foreground font-semibold">Status</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredData.map((row, index) => (
                <motion.tr
                  key={row.id}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.05 }}
                  className="border-border/30 hover:bg-muted/20 transition-colors"
                >
                  <TableCell className="font-mono text-sm">{row.cnpj}</TableCell>
                  <TableCell>{row.razaoSocial}</TableCell>
                  <TableCell className="font-medium">{row.valor}</TableCell>
                  <TableCell>
                    <Badge className={cn("border", getStatusColor(row.status))}>
                      {row.status.charAt(0).toUpperCase() + row.status.slice(1)}
                    </Badge>
                  </TableCell>
                </motion.tr>
              ))}
            </TableBody>
          </Table>
        </div>

        <div className="flex items-center justify-between mt-4 text-sm text-muted-foreground">
          <span>{filteredData.length} registros encontrados</span>
          <Button variant="outline" size="sm" className="glass-card">
            <Download className="w-4 h-4 mr-2" />
            Exportar
          </Button>
        </div>
      </motion.div>
    </motion.div>
  )
}

// Log Tab
function LogTab({
  logs,
  onClearLogs,
  getLogIcon,
}: {
  logs: LogEntry[]
  onClearLogs: () => void
  getLogIcon: (type: LogEntry["type"]) => React.ReactNode
}) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      className="space-y-6"
    >
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className="glass-card rounded-2xl p-6 h-[calc(100vh-200px)]"
      >
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-lg font-semibold flex items-center gap-2">
            <Terminal className="w-5 h-5 text-primary" />
            Log de Execução Completo
          </h2>
          <div className="flex items-center gap-3">
            <Button variant="outline" size="sm" className="glass-card">
              <Download className="w-4 h-4 mr-2" />
              Exportar Log
            </Button>
            <Button
              variant="outline"
              size="sm"
              onClick={onClearLogs}
              className="glass-card hover:bg-red-500/20 hover:border-red-500/30"
            >
              <Trash2 className="w-4 h-4 mr-2" />
              Limpar
            </Button>
          </div>
        </div>

        <div className="bg-background/50 rounded-xl p-4 h-[calc(100%-80px)] overflow-y-auto font-mono text-sm">
          {logs.map((log, index) => (
            <motion.div
              key={log.id}
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.02 }}
              className="flex items-start gap-3 py-2 border-b border-border/20 last:border-0"
            >
              {getLogIcon(log.type)}
              <span className="text-muted-foreground min-w-[80px]">{log.timestamp}</span>
              <span className={cn(
                "flex-1",
                log.type === "success" && "text-emerald-400",
                log.type === "warning" && "text-amber-400",
                log.type === "error" && "text-red-400",
                log.type === "info" && "text-foreground"
              )}>
                {log.message}
              </span>
            </motion.div>
          ))}
        </div>
      </motion.div>
    </motion.div>
  )
}

// Histórico Tab
function HistoricoTab({
  history,
  getStatusColor,
}: {
  history: ProcessingRecord[]
  getStatusColor: (status: string) => string
}) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      className="space-y-6"
    >
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className="glass-card rounded-2xl p-6"
      >
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-lg font-semibold flex items-center gap-2">
            <History className="w-5 h-5 text-primary" />
            Histórico de Processamentos
          </h2>
          <Button variant="outline" size="sm" className="glass-card">
            <RefreshCw className="w-4 h-4 mr-2" />
            Atualizar
          </Button>
        </div>

        <div className="space-y-3">
          {history.map((record, index) => (
            <motion.div
              key={record.id}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className="glass p-4 rounded-xl flex items-center justify-between hover:bg-muted/20 transition-all duration-300"
            >
              <div className="flex items-center gap-4">
                <div className={cn(
                  "w-10 h-10 rounded-xl flex items-center justify-center",
                  record.status === "success" && "bg-emerald-500/20",
                  record.status === "error" && "bg-red-500/20",
                  record.status === "processing" && "bg-amber-500/20"
                )}>
                  {record.status === "success" && <CheckCircle2 className="w-5 h-5 text-emerald-400" />}
                  {record.status === "error" && <X className="w-5 h-5 text-red-400" />}
                  {record.status === "processing" && <RefreshCw className="w-5 h-5 text-amber-400 animate-spin" />}
                </div>
                <div>
                  <p className="font-medium">{record.fileName}</p>
                  <p className="text-sm text-muted-foreground">{record.date}</p>
                </div>
              </div>
              <div className="flex items-center gap-6">
                <div className="text-right">
                  <p className="font-medium">{record.records} registros</p>
                  <p className="text-sm text-muted-foreground">{record.duration}</p>
                </div>
                <Badge className={cn("border", getStatusColor(record.status))}>
                  {record.status === "success" && "Sucesso"}
                  {record.status === "error" && "Erro"}
                  {record.status === "processing" && "Processando"}
                </Badge>
              </div>
            </motion.div>
          ))}
        </div>
      </motion.div>
    </motion.div>
  )
}

// Usuário Tab
function UsuarioTab({ user }: { user: typeof import("./nfse-automation").NFSeAutomation extends () => infer R ? never : { name: string; email: string; role: string; avatar: string; lastLogin: string; totalProcessed: number; successRate: number } }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      className="space-y-6"
    >
      {/* User Profile Card */}
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className="glass-card rounded-2xl p-8"
      >
        <div className="flex items-start gap-6">
          <div className="relative">
            <Avatar className="w-24 h-24 border-4 border-primary/30">
              <AvatarImage src={user.avatar} alt={user.name} />
              <AvatarFallback className="text-2xl bg-gradient-to-br from-primary to-accent text-primary-foreground">
                {user.name.split(" ").map(n => n[0]).join("")}
              </AvatarFallback>
            </Avatar>
            <div className="absolute -bottom-1 -right-1 w-6 h-6 bg-emerald-500 rounded-full border-4 border-card flex items-center justify-center">
              <div className="w-2 h-2 bg-white rounded-full" />
            </div>
          </div>
          <div className="flex-1">
            <h2 className="text-2xl font-bold">{user.name}</h2>
            <p className="text-muted-foreground">{user.email}</p>
            <Badge className="mt-2 bg-primary/20 text-primary border-primary/30">{user.role}</Badge>
          </div>
          <Button variant="outline" className="glass-card">
            <Settings className="w-4 h-4 mr-2" />
            Editar Perfil
          </Button>
        </div>
      </motion.div>

      {/* Stats Grid */}
      <div className="grid grid-cols-3 gap-4">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="glass-card rounded-2xl p-6"
        >
          <div className="flex items-center gap-3 mb-2">
            <div className="w-10 h-10 rounded-xl bg-primary/20 flex items-center justify-center">
              <Clock className="w-5 h-5 text-primary" />
            </div>
            <span className="text-muted-foreground">Último acesso</span>
          </div>
          <p className="text-xl font-bold">{user.lastLogin}</p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="glass-card rounded-2xl p-6"
        >
          <div className="flex items-center gap-3 mb-2">
            <div className="w-10 h-10 rounded-xl bg-emerald-500/20 flex items-center justify-center">
              <FileSpreadsheet className="w-5 h-5 text-emerald-400" />
            </div>
            <span className="text-muted-foreground">Total processado</span>
          </div>
          <p className="text-xl font-bold">{user.totalProcessed.toLocaleString()}</p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="glass-card rounded-2xl p-6"
        >
          <div className="flex items-center gap-3 mb-2">
            <div className="w-10 h-10 rounded-xl bg-cyan-500/20 flex items-center justify-center">
              <CheckCircle2 className="w-5 h-5 text-cyan-400" />
            </div>
            <span className="text-muted-foreground">Taxa de sucesso</span>
          </div>
          <p className="text-xl font-bold text-emerald-400">{user.successRate}%</p>
        </motion.div>
      </div>
    </motion.div>
  )
}
