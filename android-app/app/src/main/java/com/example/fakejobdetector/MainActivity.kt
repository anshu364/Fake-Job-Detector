package com.example.fakejobdetector

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.example.fakejobdetector.ui.theme.FakeJobDetectorTheme
import kotlinx.coroutines.MainScope
import kotlinx.coroutines.launch
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import org.json.JSONObject
import java.net.HttpURLConnection
import java.net.URL
import java.net.URLEncoder

class MainActivity : ComponentActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        setContent {
            FakeJobDetectorTheme {
                FakeJobDetectorApp()
            }
        }
    }
}

@Composable
fun FakeJobDetectorApp() {

    var jobText by remember { mutableStateOf("") }
    var result by remember { mutableStateOf<AnalysisResult?>(null) }
    var loading by remember { mutableStateOf(false) }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState())
            .padding(20.dp)
    ) {

        Text(
            text = "AI Fake Job & Internship Detector",
            style = MaterialTheme.typography.headlineSmall
        )

        Spacer(modifier = Modifier.height(8.dp))

        Text(
            text = "Check the estimated risk of a job or internship posting.",
            style = MaterialTheme.typography.bodyMedium
        )

        Spacer(modifier = Modifier.height(20.dp))

        OutlinedTextField(
            value = jobText,
            onValueChange = { jobText = it },
            label = {
                Text("Job / Internship Description")
            },
            placeholder = {
                Text("Paste the job description here...")
            },
            modifier = Modifier
                .fillMaxWidth()
                .height(200.dp)
        )

        Spacer(modifier = Modifier.height(16.dp))

        Button(
            onClick = {

                loading = true
                result = null

                MainScope().launch {

                    result = analyzeJob(jobText)

                    loading = false
                }
            },
            enabled = jobText.isNotBlank() && !loading,
            modifier = Modifier.fillMaxWidth()
        ) {

            if (loading) {

                CircularProgressIndicator(
                    modifier = Modifier.size(20.dp),
                    strokeWidth = 2.dp
                )

            } else {

                Text("Analyze Job")
            }
        }

        Spacer(modifier = Modifier.height(24.dp))

        result?.let { data ->

            Card(
                modifier = Modifier.fillMaxWidth(),
                elevation = CardDefaults.cardElevation(
                    defaultElevation = 4.dp
                )
            ) {

                Column(
                    modifier = Modifier.padding(20.dp)
                ) {

                    Text(
                        text = "Analysis Result",
                        style = MaterialTheme.typography.titleLarge
                    )

                    Spacer(modifier = Modifier.height(16.dp))

                    Text(
                        text = "Risk Score",
                        style = MaterialTheme.typography.labelLarge
                    )

                    Spacer(modifier = Modifier.height(4.dp))

                    Text(
                        text = "${"%.2f".format(data.riskScore)}%",
                        style = MaterialTheme.typography.headlineMedium
                    )

                    Spacer(modifier = Modifier.height(16.dp))

                    Text(
                        text = "Risk Level",
                        style = MaterialTheme.typography.labelLarge
                    )

                    Spacer(modifier = Modifier.height(4.dp))

                    Text(
                        text = data.riskLevel,
                        style = MaterialTheme.typography.titleMedium
                    )

                    Spacer(modifier = Modifier.height(16.dp))

                    Text(
                        text = "Prediction",
                        style = MaterialTheme.typography.labelLarge
                    )

                    Spacer(modifier = Modifier.height(4.dp))

                    Text(
                        text = data.prediction,
                        style = MaterialTheme.typography.bodyLarge
                    )

                    Spacer(modifier = Modifier.height(20.dp))

                    Text(
                        text = "Suspicious Indicators",
                        style = MaterialTheme.typography.titleMedium
                    )

                    Spacer(modifier = Modifier.height(8.dp))

                    if (data.indicators.isEmpty()) {

                        Text(
                            text = "✓ No obvious suspicious indicators detected.",
                            style = MaterialTheme.typography.bodyMedium
                        )

                    } else {

                        data.indicators.forEach { indicator ->

                            Text(
                                text = "• $indicator",
                                style = MaterialTheme.typography.bodyMedium,
                                modifier = Modifier.padding(vertical = 3.dp)
                            )
                        }
                    }

                    Spacer(modifier = Modifier.height(20.dp))

                    HorizontalDivider()

                    Spacer(modifier = Modifier.height(12.dp))

                    Text(
                        text = "Disclaimer",
                        style = MaterialTheme.typography.labelLarge
                    )

                    Spacer(modifier = Modifier.height(4.dp))

                    Text(
                        text = "This is an AI-based risk assessment and does not prove that a job posting is fraudulent.",
                        style = MaterialTheme.typography.bodySmall
                    )
                }
            }
        }
    }
}

data class AnalysisResult(
    val riskScore: Double,
    val riskLevel: String,
    val prediction: String,
    val indicators: List<String>
)

suspend fun analyzeJob(jobText: String): AnalysisResult? {

    return withContext(Dispatchers.IO) {

        try {

            val encodedText = URLEncoder.encode(
                jobText,
                "UTF-8"
            )

            val url = URL(
                "https://fake-job-detector-t320.onrender.com/analyze?job_text=$encodedText"
            )

            val connection =
                url.openConnection() as HttpURLConnection

            connection.requestMethod = "POST"
            connection.connectTimeout = 30000
            connection.readTimeout = 30000

            if (connection.responseCode == 200) {

                val response = connection.inputStream
                    .bufferedReader()
                    .use { it.readText() }

                val json = JSONObject(response)

                val indicatorsJson =
                    json.getJSONArray("suspicious_indicators")

                val indicators = mutableListOf<String>()

                for (i in 0 until indicatorsJson.length()) {

                    indicators.add(
                        indicatorsJson.getString(i)
                    )
                }

                AnalysisResult(
                    riskScore = json.getDouble("risk_score"),
                    riskLevel = json.getString("risk_level"),
                    prediction = json.getString("prediction"),
                    indicators = indicators
                )

            } else {

                null
            }

        } catch (e: Exception) {

            null
        }
    }
}